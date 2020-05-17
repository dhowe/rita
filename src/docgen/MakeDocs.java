package docgen;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.zip.GZIPOutputStream;

import processing.core.PApplet;
import processing.data.JSONArray;
import processing.data.JSONObject;

public class MakeDocs extends PApplet
{
  static final String OUTPUT_TYPE = "html";
  static final String VERSION = "2.01";
  static final boolean OUTPUT_MARKUP = false;
  static String DATA_DIR = "data", OUTPUT_DIR = "/tmp/";
  static int numOfMethods, numOfparameters, numOfReturns;
  static String[] lines, methodName, example, description, syntax,
      parameterType, parameterDesc, parameters, theReturn, returnType,
      returnDesc, returns, related, thePlatform, note, parameter;
  static boolean[] hidden, isVariable;
  static String outputTemplate;
  static String[] CLASS_NAMES = { "RiTa", "RiGrammar", "RiMarkov" };
  static Map<String, ArrayList<String>> API = new HashMap<String, ArrayList<String>>();
  static boolean DBUG = false;

  static {
    System.out.println("[INFO] DocGen.version [" + VERSION + "]");
  }

  // ////////////////////////////////////////////////////////////////

  public static void go(String[] a)
  {
    if (a.length < 1) {
      System.out.println("\nusage: java rita.docgen.MakeDocs output-dir [input-dir]\n");
      System.exit(1);
    } else {
      pln("\nCWD: " + System.getProperty("user.dir"));

      OUTPUT_DIR = a[0];

      if (a.length > 1) DATA_DIR = a[1];

      pln("DATA: " + DATA_DIR);
      pln("OUTPUT: " + OUTPUT_DIR);

      if (a.length > 2) {
        CLASS_NAMES = new String[] { a[2] };
        pln("CLASSES: " + Arrays.asList(CLASS_NAMES));
      }
    }

    outputTemplate = DATA_DIR + "/template." + OUTPUT_TYPE;
    System.out.println("Files to generate: " + CLASS_NAMES.length);
    parseAPI();
    if (1 == 1) return;
    for (int i = 0; i < CLASS_NAMES.length; i++) {
      pln("\n******     " + CLASS_NAMES[i] + "     ******\n");
      pln("  Template : " + outputTemplate);
      parseJSON(CLASS_NAMES[i]);
    }

    pln("\nDONE: files written to " + OUTPUT_DIR +
        "*." + OUTPUT_TYPE + " (from " + System.getProperty("user.dir") + ")");
  }

  static void parseAPI()
  {
    try {
      String jsonFile = DATA_DIR + "/API.json";
      String result = stringFrom(jsonFile);
      // result = "{ \"success\": true, \"pagination\": { \"current\": 1,
      // \"max\": 1 }, \"refobj\": " + result + "}";
      JSONObject raw = JSONObject.parse(result);
      JSONArray classes = raw.getJSONArray("classes");
      if (classes != null) {
        int numOfClasses = classes.size();
        for (int j = 0; j < numOfClasses; j++) {
          JSONObject c = classes.getJSONObject(j);
          String className = c.getString("class");
          pln("  Class : " + className);

          ArrayList<String> tmp = null;
          JSONArray fields = c.getJSONArray("fields");
          if (fields != null) {
            tmp = new ArrayList<String>();
            for (int k = 0; k < fields.size(); k++) {
              String name = fields.getString(k);
              tmp.add(name);
              pln("    " + name);
            }
            API.put(className + ".fields", tmp);
          }
          JSONArray statics = c.getJSONArray("statics");
          if (statics != null) {
            tmp = new ArrayList<String>();
            for (int k = 0; k < statics.size(); k++) {
              String name = statics.getString(k);
              tmp.add(name);
              pln("    " + name);
            }
            API.put(className + ".statics", tmp);
          }
          JSONArray functions = c.getJSONArray("functions");
          if (functions != null) {
            tmp = new ArrayList<String>();
            for (int k = 0; k < functions.size(); k++) {
              String name = functions.getString(k);
              tmp.add(name);
              pln("    " + name);
            }
            API.put(className + ".functions", tmp);
          }
        }
      }
    } catch (Exception e) {
      System.err.println("\nError parsing the JSONObject!");
      throw new RuntimeException(e);
    }
  }

  static void parseJSON(String shortName)
  {
    String jsonFile = DATA_DIR + "/" + shortName + ".json";

    try {

      pln("  DocFile : " + jsonFile);
      String result = stringFrom(jsonFile);

      result = "{ \"success\": true, \"pagination\": { \"current\": 1, \"max\": 1 }, \"refobj\": " + result + "}";

      JSONObject raw = JSONObject.parse(result);
      JSONObject json = raw.getJSONObject("refobj");

      String className = json.getString("class");
      pln("  Class : " + className);

      JSONArray items = json.getJSONArray("fields");
      if (items != null) {
        numOfMethods = items.size();

        pln("  Fields(" + numOfMethods + ") : ");

        initArrays();

        for (int j = 0; j < numOfMethods; j++) {
          lines = stringsFrom(outputTemplate);

          JSONObject entry = items.getJSONObject(j);

          hidden[j] = false;
          if (!entry.isNull("hidden")) {
            hidden[j] = entry.getBoolean("hidden");
          }

          isVariable[j] = false;
          if (!entry.isNull("variable")) {
            isVariable[j] = entry.getBoolean("variable");
          }

          methodName[j] = entry.getString("name");
          pln("    " + methodName[j]);

          example[j] = "";
          if (!entry.isNull("example")) {
            example[j] = entry.getString("example");
          }

          description[j] = entry.getString("description");
          syntax[j] = entry.getString("syntax");

          JSONArray parametersJSON = entry.getJSONArray("parameters");
          numOfparameters = parametersJSON.size();
          parameter = new String[numOfparameters];
          parameterType = new String[numOfparameters];
          parameterDesc = new String[numOfparameters];

          for (int k = 0; k < numOfparameters; k++) {
            JSONObject parametersJSONEntry = parametersJSON.getJSONObject(k);
            parameterType[k] = parametersJSONEntry.getString("type");
            parameterDesc[k] = parametersJSONEntry.getString("desc");
          }

          JSONArray returnsJSON = entry.getJSONArray("returns");
          numOfReturns = returnsJSON.size();
          theReturn = new String[numOfReturns];
          returnType = new String[numOfReturns];
          returnDesc = new String[numOfReturns];
          for (int k = 0; k < numOfReturns; k++) {
            JSONObject returnsJSONEntry = returnsJSON.getJSONObject(k);
            returnType[k] = returnsJSONEntry.getString("type");
            returnDesc[k] = returnsJSONEntry.getString("desc");
          }
          related[j] = entry.getString("related");
          thePlatform[j] = entry.getString("platform");
          note[j] = entry.getString("note");

          template(j, shortName);

          plnMarkup(shortName, methodName[j], isVariable[j]);
        }
      }
    } catch (Exception e) {
      System.err.println("\nError parsing the JSONObject!");
      throw new RuntimeException(e);
    }
  }

  static String stringFrom(String fname) throws Exception
  {
    Stream<String> lines = Files.lines(Paths.get(fname));
    String result = lines.collect(Collectors.joining("\n"));
    lines.close();
    return result;
  }

  static String[] stringsFrom(String fname) throws Exception
  {
    Stream<String> lines = Files.lines(Paths.get(fname));
    String[] result = lines.toArray(String[]::new);
    lines.close();
    return result;
  }

  // ----------------------------------------------------------------------
  static void initArrays()
  {
    methodName = new String[numOfMethods];
    example = new String[numOfMethods];
    description = new String[numOfMethods];
    syntax = new String[numOfMethods];
    parameters = new String[numOfMethods];
    returns = new String[numOfMethods];
    related = new String[numOfMethods];
    thePlatform = new String[numOfMethods];
    note = new String[numOfMethods];
    hidden = new boolean[numOfMethods];
    isVariable = new boolean[numOfMethods];
  }

  static public PrintWriter createWriter(File file)
  {
    if (file == null)
      throw new RuntimeException("null File passed to createWriter()");

    try {
      createPath(file); // make sure in-between folders exist
      OutputStream output = new FileOutputStream(file);
      if (file.getName().toLowerCase().endsWith(".gz")) {
        output = new GZIPOutputStream(output);
      }
      return createWriter(output);

    } catch (Exception e) {
      e.printStackTrace();
      throw new RuntimeException("Couldn't create writer for " + file.getAbsolutePath());
    }
  }

  static void template(int idx, String shortName)
  {
    if (hidden[idx]) return;

    String folder_methodName = methodName[idx].replaceAll("\\(\\)", "_");

    String fname = OUTPUT_DIR + "/" + shortName + "/" + folder_methodName + "/index." + OUTPUT_TYPE;

    lines = replaceArr(lines, "tmp_ext", OUTPUT_TYPE);
    lines = replaceArr(lines, "tmp_className", shortName);
    lines = replaceArr(lines, "tmp_methodName", methodName[idx]);
    lines = replaceArr(lines, "tmp_description", description[idx]);
    lines = replaceArr(lines, "tmp_platform", thePlatform[idx]);

    handleOptionalTag("example", example[idx]);
    handleOptionalTag("syntax", syntax[idx]);
    handleOptionalTag("related", related[idx]);
    handleOptionalTag("note", note[idx]);

    handleParameters(parameters[idx]);
    handleReturns(returns[idx]);

    if (isVariable[idx])
      lines = replaceArr(lines, "<th scope=\"row\">Returns</th>", "<th scope=\"row\">Type</th>");

    writeFile(fname, lines);
  }

  private static void writeFile(String fname, String[] theLines)
  {
    PrintWriter output = createWriter(new File(fname));
    for (int i = 0; i < theLines.length; i++) {
      output.println(theLines[i]);
    }
    output.flush();
    output.close();
  }

  private static void handleParameters(String data)
  {
    if (numOfparameters < 1) {
      lines = replaceArr(lines, "<tr class='Parameters'>", "<tr class='Parameters' style='display:none'>");
      return;
    }

    for (int i = 0; i < lines.length; i++) {
      String[] m = match(lines[i], "tmp_parameters");
      if (m != null) {
        for (int k = 0; k < numOfparameters; k++) {
          parameter[k] = "<tr class=''><th width='25%' scope='row' class=nobold>" + parameterType[k]
              + "</th><td width='75%'>" + parameterDesc[k] + "</td></tr>";

          data = data == null ? "" : data;
          data += parameter[k];
        }

        if (parameters != null)
          lines[i] = lines[i].replaceAll("tmp_parameters", data);
      }
    }
  }

  private static void handleReturns(String data)
  {
    if (returnType.length == 0 || returnType[0].length() == 0) {
      lines = replaceArr(lines, "tmp_returns", "void");
      return;
    }

    for (int i = 0; i < lines.length; i++) {
      String[] m2 = match(lines[i], "tmp_returns");

      if (m2 != null) {
        for (int k = 0; k < numOfReturns; k++) {
          theReturn[k] = "<tr class=''><th width='25%' scope='row' class=nobold>" + returnType[k]
              + "</th><td width='75%'>" + returnDesc[k] + "</td></tr>";

          data = data == null ? "" : data;
          data += theReturn[k];
        }

        if (returns != null)
          lines[i] = lines[i].replaceAll("tmp_returns", data);
      }
    }
  }

  static void handleOptionalTag(String name, String data)
  {

    String uname = upperCaseFirst(name);
    lines = (data.length() > 0) ? replaceArr(lines, "tmp_" + name, data) : replaceArr(lines, "<tr class='" + uname + "'>", "<tr class='" + uname + "' style='display:none'>");
  }

  static String upperCaseFirst(String value)
  {

    return Character.toString(value.charAt(0)).toUpperCase() + value.substring(1);
  }

  static String[] replaceArr(String[] in, String from, String to)
  {

    String delim = "_XXX_"; // hack
    String joined = String.join(delim, in);
    joined = joined.replaceAll(from, to);
    return joined.split(delim);
  }

  private static void pln(String s)
  {
    if (!OUTPUT_MARKUP) System.out.println(s);
  }

  private static void plnMarkup(String classShortName, String field, boolean isVar)
  {
    if (OUTPUT_MARKUP) {
      field = field.replaceAll("\\(\\)", "");
      StringBuilder sb = new StringBuilder();
      sb.append("<a href=\"" + classShortName + "/");
      sb.append(field + "_/index." + OUTPUT_TYPE + "\">" + field);
      if (!isVar) sb.append("()");
      sb.append("</a>");
      System.out.println(sb.toString());
    }
  }

  public static void main(String[] args)
  {
    // System.out.println("ARGS: "+Arrays.asList(args));

    if (args.length == 0) {
      go(new String[] { "ref/", DATA_DIR }); // ALL
      // go(new String[] {OUTPUT_DIR, DATA_DIR,"RiWordNet"}); // ONE
    } else {
      go(args);
    }
  }

}

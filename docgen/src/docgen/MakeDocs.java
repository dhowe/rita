package docgen;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.zip.GZIPOutputStream;

import processing.core.PApplet;
import processing.data.JSONArray;
import processing.data.JSONObject;

public class MakeDocs extends PApplet {

	static String DATA_DIR = "data";
	static String STATIC_DIR = "static";
	static String WWW_OUTPUT = "../dist/";
	static String REF_OUTPUT = "reference/";
	static String[] CLASS_NAMES = { "RiTa", "Grammar", "Markov" };

	static String FUNCTION_TEMPLATE = "function.tmpl";
	static String REFINDEX_TEMPLATE = "refindex.tmpl";
	static String WWWINDEX_TEMPLATE = "ritahome.tmpl";

	static boolean DBUG = false, OUTPUT_MARKUP = false;
	static final String OUTPUT_TYPE = "html";
	static boolean SILENT = false;

	static String[] types = new String[] { "functions", "statics", "fields" };

	static String[] lines, methodName, example, description, syntax, thePlatform;
	static String[] returnType, returnDesc, returns, related, note, parameter;
	static String[] parameterType, parameterDesc, parameters, theReturn;
	static int numOfMethods, numOfparameters, numOfReturns;

	static boolean[] hidden, isVariable;
	static Map<String, ArrayList<String>> API;
	static String outputTemplate, warnings = "", errors = "";

	static {
		API = new HashMap<String, ArrayList<String>>();
	}

	// ////////////////////////////////////////////////////////////////

	static void writeIndex() {

		//if (1==1) throw new RuntimeException("Invalid foo");

		String[] templates = {
				DATA_DIR + "/" + REFINDEX_TEMPLATE,  // reference index
				DATA_DIR + "/" + WWWINDEX_TEMPLATE // homepage index
		};
		String[] outputs = {
				WWW_OUTPUT + REF_OUTPUT + "index." + OUTPUT_TYPE,  // reference index
				WWW_OUTPUT + "index." + OUTPUT_TYPE   // homepage index
		};

		for (int f = 0; f < templates.length; f++) {

			String[] tmpl = stringsFrom(templates[f]);
			String contents = "";
			for (int i = 0; i < CLASS_NAMES.length; i++) {
				String cls = CLASS_NAMES[i];
				String dls = CLASS_NAMES[i] == "RiTa" ? cls : "RiTa." + cls;
				contents += "<div class=\"section\">\n";
				contents += "  <div class=\"category\">\n";
				contents += "    <span style=\"color: #006B8F !important;\"><b>" + dls +"</b><span><br><br>\n"; // no link
				for (int j = 0; j < types.length; j++) {
					ArrayList<String> entries = API.get(cls + "." + types[j]);
					for (int k = 0; entries != null && k < entries.size(); k++) {
						//String dsp = types[j] == "functions" ? ent : cls + "." + ent;
						String dsp = entries.get(k);
						if (!dsp.toUpperCase().equals(cls.toUpperCase())) {
							String href = REF_OUTPUT + cls + "/" + dsp + "/index." + OUTPUT_TYPE;
							if (types[j] == "functions" || types[j] == "statics") {
								dsp += "()";
							}
							if (types[j] != "functions") {
								dsp = cls + "." + dsp;
							}
							//pln("LINK: " + href); 
							contents += "    <a href=\"" + href + "\">" + dsp + "</a><br/>\n";
							//if (k == 0 && types[j] == "static") contents += "  <br/>\n";
							if (k == 19) {  // longest column
								contents += "  </div>\n";
								contents += "</div>\n\n";
								contents += "<div class=\"section\">\n";
								contents += "  <div class=\"category\">\n<br><br>\n";
							}
						}
					}
				}
				contents += "    <br/><br/>\n</div>\n";
				contents += "</div>\n\n";
			}
			tmpl = replaceArr(tmpl, "tmp_contents", contents);
			writeFile(outputs[f], tmpl);

		}
	}

	static void parseAPI() {

		String jsonFile = DATA_DIR + "/API.json";
		String result = stringFrom(jsonFile);
		JSONObject raw = JSONObject.parse(result);
		JSONArray classes = raw.getJSONArray("classes");
		if (classes != null) {
			pln("API:");
			int numOfClasses = classes.size();
			for (int j = 0; j < numOfClasses; j++) {
				JSONObject c = classes.getJSONObject(j);
				String className = c.getString("class");
				pln("  " + className);

				for (int i = 0; i < types.length; i++) {
					JSONArray fields = c.getJSONArray(types[i]);
					// pln("CHECK: " + className + "." + types[i]);
					if (fields != null) {
						ArrayList<String> tmp = new ArrayList<String>();
						for (int k = 0; k < fields.size(); k++) {
							String name = fields.getString(k);
							tmp.add(name);
							pln("    " + name);
						}
						API.put(className + "." + types[i], tmp);
					}
				}
			}
		}

	}

	static void parseJSON(String shortName) {
		String jsonFile = DATA_DIR + "/" + shortName + ".json";

		pln("  DocFile : " + jsonFile);
		String result = stringFrom(jsonFile);

		result = "{ \"success\": true, \"pagination\": { \"current\": 1, \"max\": 1 }, \"refobj\": " + result + "}";

		JSONObject raw = JSONObject.parse(result);
		JSONObject json = raw.getJSONObject("refobj");

		String className = json.getString("class");
		pln("  Class : " + className);

		for (int i = 0; i < types.length; i++) {
			processEntry(types[i], shortName, json);
		}

	}

	private static void processEntry(String type, String shortName, JSONObject json) {
		JSONArray items = json.getJSONArray(type);
		ArrayList<String> check = API.get(shortName + "." + type);
		ArrayList<String> extra = new ArrayList<String>();

		if (items != null && items.size() > 0) {

			numOfMethods = items.size();
			initArrays();

			pln("  " + ucf(type) + "(" + numOfMethods + ") : ");

			for (int j = 0; j < numOfMethods; j++) {

				JSONObject entry = items.getJSONObject(j);

				methodName[j] = entry.getString("name");
				pln("    " + methodName[j]);

				if (check != null && check.contains(methodName[j])) {
					check.remove(methodName[j]);
				}
				else {
					extra.add(methodName[j]);
				}

				hidden[j] = false;
				if (!entry.isNull("hidden")) {
					hidden[j] = entry.getBoolean("hidden");
				}

				isVariable[j] = false;
				if (!entry.isNull("variable")) {
					isVariable[j] = entry.getBoolean("variable");
				}

				example[j] = "";
				if (!entry.isNull("example")) {
					example[j] = entry.getString("example");
				}

				description[j] = entry.getString("description");
				if (description[j].length() == 0) {
					warnings += "Missing Desc: " + shortName + "." + methodName[j] + "()\n";
				}
				syntax[j] = entry.getString("syntax");
				if (syntax[j].length() == 0) {
					warnings += "Missing Syntax: " + shortName + "." + methodName[j] + "()\n";
				}

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
				if (thePlatform[j] == null || thePlatform[j].length() == 0) {
					thePlatform[j] = "Java / JavaScript";
				}
				note[j] = entry.getString("note");

				lines = stringsFrom(outputTemplate);

				template(j, shortName);

				plnMarkup(shortName, methodName[j], isVariable[j]);
			}

			if (extra.size() > 0)
				errors += shortName + " has extra docs: " + extra + "\n";
			if (check != null && check.size() > 0)
				errors += shortName + " has missing docs: " + check + "\n";
		}

	}

	private static String ucf(String s) {
		return (s.charAt(0) + "").toUpperCase() + s.substring(1);
	}

	static String stringFrom(String fname) {
		try {
			Stream<String> lines = Files.lines(Paths.get(fname));
			String result = lines.collect(Collectors.joining("\n"));
			lines.close();
			return result;
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}

	static String[] stringsFrom(String fname) {
		try {
			Stream<String> lines = Files.lines(Paths.get(fname));
			String[] result = lines.toArray(String[]::new);
			lines.close();
			return result;
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}

	// ----------------------------------------------------------------------
	static void initArrays() {
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

	static public PrintWriter createWriter(File file) {

		try {
			createPath(file); // make sure in-between folders exist
			OutputStream output = new FileOutputStream(file);
			if (file.getName().toLowerCase().endsWith(".gz")) {
				output = new GZIPOutputStream(output);
			}
			return createWriter(output);
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	// static void template(int idx, String shortName, String[] lines) {
	static void template(int idx, String shortName) {
		if (hidden[idx]) return;

		String folderMethodName = methodName[idx].replaceAll("\\(\\)", "_");

		String fname = WWW_OUTPUT + REF_OUTPUT + "/" + shortName + "/" + folderMethodName + "/index." + OUTPUT_TYPE;

		lines = replaceArr(lines, "tmp_ext", OUTPUT_TYPE);
		lines = replaceArr(lines, "tmp_className", shortName);
		lines = replaceArr(lines, "tmp_description", description[idx]);
		lines = replaceArr(lines, "tmp_platform", thePlatform[idx]);
		if (!methodName[idx].toUpperCase().equals(shortName.toUpperCase())) {
			lines = replaceArr(lines, "tmp_methodName", methodName[idx]);
		}

		if (shortName.equals("RiTa")) {
			lines = replaceArr(lines, "<a href=\"../../RiTa/RiTa/index.html\">RiTa</a>", "RiTa");
		}

		optionalTag("example", example[idx]);
		optionalTag("syntax", syntax[idx]);
		optionalTag("related", related[idx]);
		optionalTag("note", note[idx]);
		if (methodName[idx].toUpperCase().equals(shortName.toUpperCase())) {
			optionalTag("method name", "");
		}

		handleParameters(parameters[idx]);
		handleReturns(returns[idx]);

		if (isVariable[idx]) {
			lines = replaceArr(lines, "<th scope=\"row\">Returns</th>", "<th scope=\"row\">Type</th>");
		}

		writeFile(fname, lines);
	}

	private static void writeFile(String fname, String[] theLines) {
		// pln("Writing " + fname);
		PrintWriter output = createWriter(new File(fname));
		for (int i = 0; i < theLines.length; i++) {
			output.println(theLines[i]);
		}
		output.flush();
		output.close();
	}

	private static void handleParameters(String data) {
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

	private static void handleReturns(String data) {
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

	static void optionalTag(String name, String data) {
		String uname = upperCaseFirst(name);
		if (name.equals("method name")) {
			lines = replaceArr(lines, "<tr class=\"name-row\">", "<tr class=\"name-row\" style='display:none'>");
		}
		else {
			lines = (data != null && data.length() > 0) ? replaceArr(lines, "tmp_" + name, data)
					: replaceArr(lines, "<tr class='" + uname + "'>", "<tr class='" + uname + "' style='display:none'>");
		}
	}

	static String upperCaseFirst(String value) {
		return (value != null) ? Character.toString(value.charAt(0)).toUpperCase() + value.substring(1) : "";
	}

	static String[] replaceArr(String[] in, String from, String to) {
		String delim = "_XXX_"; // hack
		String joined = String.join(delim, in);
		if (to.contains("$")) {
			joined = joined.replaceAll(from, Matcher.quoteReplacement(to));
		}
		else {
			joined = joined.replaceAll(from, to);
		}
		return joined.split(delim);
	}

	private static void pln(String s) {
		if (!OUTPUT_MARKUP && !SILENT) {
			System.out.println(s);
		}
	}

	static void copyFolder(String from, String to) {
		try {
			// source & destination directories
			Path src = Paths.get(from + "/");
			Path dest = Paths.get(to);

			pln("\nCopying statics from " + src + " to " + dest);

			// create stream for `src`
			Stream<Path> files = Files.walk(src).filter(Files::isRegularFile);

			// copy all files and folders from `src` to `dest`
			files.forEach(file -> {
				try {
					Files.copy(file, dest.resolve(src.relativize(file)),
							StandardCopyOption.REPLACE_EXISTING);
				} catch (IOException e) {
					throw new RuntimeException(e);
				}
			});
			files.close();
		} catch (IOException ex) {
			throw new RuntimeException(ex);
		}
	}

	private static void plnMarkup(String classShortName, String field, boolean isVar) {
		if (OUTPUT_MARKUP) {
			field = field.replaceAll("\\(\\)", "");
			StringBuilder sb = new StringBuilder();
			sb.append("<a href=\"" + classShortName + "/");
			sb.append(field + "_/index." + OUTPUT_TYPE + "\">" + field);
			if (!isVar) sb.append("()");
			sb.append("</a>");
			pln(sb.toString());
		}
	}

	public static void main(String[] args) {

		if (args != null && args.length > 0 && args[0].equals("--silent")) {
			SILENT = true;
		}

		try {
			pln("\nCWD: " + System.getProperty("user.dir"));
			pln("DATA: " + DATA_DIR);
			pln("OUTPUT: " + WWW_OUTPUT + REF_OUTPUT);

			//errors += "invalid blah";

			outputTemplate = DATA_DIR + "/" + FUNCTION_TEMPLATE;
			pln("Files to generate: " + CLASS_NAMES.length);

			parseAPI();
			writeIndex();
			// if (1 == 1) return;
			for (int i = 0; i < CLASS_NAMES.length; i++) {
				pln("\n******     " + CLASS_NAMES[i] + "     ******\n");
				pln("  Template : " + outputTemplate);
				parseJSON(CLASS_NAMES[i]);
			}

			copyFolder(STATIC_DIR, WWW_OUTPUT + REF_OUTPUT);

			if (!SILENT && errors.length() > 0) throw new RuntimeException("\n" + errors);

			pln("DONE: reference written to " + WWW_OUTPUT + REF_OUTPUT);

		} catch (Throwable e) {

			if (!SILENT) throw new RuntimeException(e);
			errors = "EXCEPTION: " + e.getMessage() + "\n" + errors;
		}

		if (warnings.length() > 0 || errors.length() > 0) {
			String msg = (warnings.length() > 0 ? "WARNING: " + warnings + "\n" : "")
					+ (errors.length() > 0 ? "ERROR: " + errors : "");
			System.err.println("\n" + msg);
			System.exit(1);
		}
		else {
			System.exit(0);
		}
	}

}

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

	static boolean SILENT = false, DBUG = false, OUTPUT_MARKUP = false;

	static String DATA_DIR = "data";
	static String TMPL_DIR = "tmpl";
	static String STATIC_DIR = "static";
	static String WWW_OUTPUT = "../pub/";
	static String REF_OUTPUT = "reference/";

	static String[] CLASS_NAMES = { "RiTa", "RiGrammar", "RiMarkov", "RiScript" };
	static String[] TYPES = { "functions", "statics", "fields" };

	static String WWWINDEX_TEMPLATE = "index.html";
	static String FUNCTION_TEMPLATE = "function.html";
	static String REFINDEX_TEMPLATE = "reference.html";

	static final String OUTPUT_TYPE = "html";
	static final String HEADER = "<!-- DOCGEN: THIS CLASS IS AUTO_GENERATED - DO NOT EDIT BY HAND! -->";

	static String[] lines, methodName, example, description, syntax, thePlatform;
	static String[] returnType, returnDesc, returns, related, note, parameter, relatedConstant;
	static String[] parameterType, parameterDesc, parameters, theReturn;
	static int numOfMethods, numOfparameters, numOfReturns;

	static boolean[] hidden, isVariable;
	static Map<String, ArrayList<String>> API;
	static String outputTemplate, warnings = "", errors = "";

	static {
		API = new HashMap<String, ArrayList<String>>();
	}

	// ////////////////////////////////////////////////////////////////

	//generate gallery
	static String generateGallery() {
		String jsonFile = DATA_DIR + "/gallery.json";
		String jsonStr = stringFrom(jsonFile);
		JSONArray raw = JSONArray.parse(jsonStr);
		ArrayList<JSONObject> listOfItem = new ArrayList<JSONObject>();
		for (int i = 0; i < raw.size(); i++) {
			listOfItem.add(raw.getJSONObject(i));
		}

		String content = "";
		String row = "";
		String col = "";
		int a = 3, b = 3, l = 0;

		for (int k = 0; k < listOfItem.size(); k += a * b) {
			content += "<div id=\"container" + k / a * b + "\" class=\"container\">\n"; 
			for (int i = 0; i < a; i++) {
				content += "	<div id=\"con" + k / a * b + "row" + i + "\" class=\"row\">\n";
				for (int j = 0; j < b; j++) {
					col = "		<div id=\"con" + k / a * b + "row" + i + "col" + j + "\" class=\"column\">\n";
					String subcontent = "";
					if (l < listOfItem.size()) {
						subcontent = "		<div class='col-md-4 gallery_home_item wow fadeInDown'>\n";
						subcontent += "				<a href='" + listOfItem.get(l).getString("link") + "' target='new'>\n";
            			subcontent += "				<img src='" + listOfItem.get(l).getString("thumb") + "'/></a><br>\n";
            			subcontent += "				<a href='" + listOfItem.get(l).getString("link") + "' target='new'>" + listOfItem.get(l).getString("title")+ "</a>\n";
            			subcontent += "				<p><span>by " + listOfItem.get(l).getString("artist") + "</span></p>\n";
						subcontent += "			</div>\n";
					} else {
						break;
					}
					l++;
					col += subcontent;
					col += "		</div>\n";
					content += col;
				}
				content += "	</div>\n";
			}
			content += "</div>\n";
		}
		return content;
	}

	static void writeIndex() {

		//if (1==1) throw new RuntimeException("Invalid foo");

		String[] templates = {
				TMPL_DIR + "/" + REFINDEX_TEMPLATE,  // reference index -> now should redirect to the homepage#reference
				TMPL_DIR + "/" + WWWINDEX_TEMPLATE // homepage index
		};
		String[] outputs = {
				WWW_OUTPUT + REF_OUTPUT + "index." + OUTPUT_TYPE,  // reference index now should redirect to the homepage#reference
				WWW_OUTPUT + "index." + OUTPUT_TYPE   // homepage index
		};

		String rslink = "https://observablehq.com/@dhowe/riscript";

		for (int f = 0; f < templates.length; f++) {

			String contents = "", tmpl[] = stringsFrom(templates[f]);

			for (int i = 0; i < CLASS_NAMES.length; i++) {

				String cls = CLASS_NAMES[i];
				contents += "<div class=\"section\">\n";
				contents += "  <div class=\"category\">\n";
				contents += "    <span style=\"color: #006B8F !important;\"><b>";
				contents += (cls.equals("RiScript") // special link for RiScript 
						? "<a href='" + rslink + "' target='_new'>[ " + cls + " ]</a></b><span>"
						: cls + "</b><span>") + "<br><br>\n";  // otherwise no link

				for (int j = 0; j < TYPES.length; j++) {

					ArrayList<String> entries = API.get(cls + "." + TYPES[j]);
					for (int k = 0; entries != null && k < entries.size(); k++) {

						String display = entries.get(k);

						if (!display.equals("toString") && !display.equals("VERSION") // skip stuff 
								&& !display.toUpperCase().equals(cls.toUpperCase())) { // skip constructors

							// f==0 means REFINDEX
							String href = (f == 0 ? "./" : REF_OUTPUT) + cls + "/" + display + "/index." + OUTPUT_TYPE;

							if (TYPES[j].equals("functions") || TYPES[j].equals("statics")) {
								display += "()";  // function or static
							}

							if (TYPES[j].equals("fields") || TYPES[j].equals("statics")) {
								if (cls.equals("RiTa")) {
									display = cls + "." + display;  // field or static (not RiTa)
									//pln("LINK: " + display);
								}
							}

							contents += "    <a href=\"" + href + "\">" + display + "</a><br/>\n";

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
			tmpl = replaceArr(tmpl, "gallery_contents", generateGallery());
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

				for (int i = 0; i < TYPES.length; i++) {
					JSONArray fields = c.getJSONArray(TYPES[i]);
					// pln("CHECK: " + className + "." + types[i]);
					if (fields != null) {
						ArrayList<String> tmp = new ArrayList<String>();
						for (int k = 0; k < fields.size(); k++) {
							String name = fields.getString(k);
							tmp.add(name);
							pln("    " + name);
						}
						API.put(className + "." + TYPES[i], tmp);
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

		for (int i = 0; i < TYPES.length; i++) {
			processEntry(TYPES[i], shortName, json);
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
				relatedConstant[j] = entry.getString("relatedConstant");

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
		relatedConstant = new String[numOfMethods];
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

		String fname = WWW_OUTPUT + REF_OUTPUT + "/" + shortName
				+ "/" + folderMethodName + "/index." + OUTPUT_TYPE;

		lines = replaceArr(lines, "tmp_ext", OUTPUT_TYPE);
		lines = replaceArr(lines, "tmp_className", shortName);
		lines = replaceArr(lines, "tmp_description", description[idx]);
		lines = replaceArr(lines, "tmp_platform", thePlatform[idx]);
		if (!methodName[idx].toUpperCase().equals(shortName.toUpperCase())) {
			lines = replaceArr(lines, "tmp_methodName", methodName[idx]);
		}

		//		if (shortName.equals("RiTa")) {
		//			lines = replaceArr(lines, "<a href=\"../../RiTa/RiTa/index.html\">RiTa</a>", "RiTa");
		//		}

		optionalTag("example", example[idx]);
		optionalTag("syntax", syntax[idx]);
		optionalTag("relatedConstant", relatedConstant[idx]);
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

	private static String[] arrayShift(String ele, String[] input) {
		List<String> tmp = new LinkedList<String>(Arrays.asList(input));
		tmp.add(0, ele);
		return tmp.toArray(new String[tmp.size()]);
	}

	private static String[] addHeader(String[] input) {
		List<String> tmp = new LinkedList<String>(Arrays.asList(input));
		tmp.add(3, "");
		tmp.add(3, HEADER);
		return tmp.toArray(new String[tmp.size()]);
	}

	private static void writeFile(String fname, String[] theLines) {
		// pln("Writing " + fname);
		theLines = addHeader(theLines);
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

	/*public static void copyDirectory(String src, String dst) {
		try {
			Files.walk(Paths.get(src)).forEach(source -> {
				Path destination = Paths.get(dst, source.toString()
						.substring(src.length()));
				try {
					System.out.println("copy("+source+","+destination+")");
					Files.copy(source, destination);
				} catch (IOException e) {
					throw new RuntimeException(e);
				}
	
			});
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}*/

	static void copyFiles(String from, String to) {
		try {
			// source & destination directories
			Path src = Paths.get(from + "/");
			Path dest = Paths.get(to);

			pln("\nCopying files from " + src + " to " + dest);

			// create stream for `src`
			Stream<Path> files = Files.walk(src).filter(Files::isRegularFile);

			// copy all files and folders from `src` to `dest`
			files.forEach(file -> {
				try {
					Path fpath = src.relativize(file);
					Files.copy(file, dest.resolve(fpath),
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

	public static void go(String[] args) {

		if (args != null && args.length > 0 && args[0].equals("--silent")) {
			SILENT = true;
		}

		try {
			pln("\nCWD: " + System.getProperty("user.dir"));
			pln("DATA_DIR: " + DATA_DIR);
			pln("TMPL_DIR: " + TMPL_DIR);
			pln("OUTPUT: " + WWW_OUTPUT + REF_OUTPUT);
			pln("CLASSES: " + Arrays.asList(CLASS_NAMES));

			parseAPI();
			writeIndex();

			outputTemplate = TMPL_DIR + "/" + FUNCTION_TEMPLATE;
			for (int i = 0; i < CLASS_NAMES.length; i++) {
				pln("\n******     " + CLASS_NAMES[i] + "     ******\n");
				pln("  Template : " + outputTemplate);
				parseJSON(CLASS_NAMES[i]);
			}

			copyFiles(STATIC_DIR, WWW_OUTPUT + REF_OUTPUT);

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

	public static void main(String[] args) {

		go(args);
	}

}

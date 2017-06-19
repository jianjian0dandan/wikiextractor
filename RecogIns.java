package com.hankcs.ml;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RecogIns {
	
	public static boolean is_title(String line) {
		if (line.startsWith("[[") && line.endsWith("]]")) {
			return true;
		}
		return false;
	}
	
	public static boolean is_section(String line) {
		if (!line.startsWith("===") && line.startsWith("==") && line.endsWith("==")) {
			return true;
		}
		return false;
	}
	
	public static boolean is_subsection(String line) {
		if (line.startsWith("===") && line.endsWith("===")) {
			return true;
		}
		return false;
	}
	
	public static boolean is_connected(String line, String title) {
		if (line.contains("机构") || line.contains("组织") || line.contains("公司")
				|| line.contains("单位")) {
			return true;
		}
		if (line.contains("成员")) {
			if (title.contains("联盟") || title.contains("聯盟"))
				return true;
		}
		
		return false;
	}
	
	public static boolean is_list_element(String line) {
		if (line.startsWith("*") || line.startsWith("#")) {
			return true;
		}
		return false;
	}
	
	public static String get_title(String line) {
		return line.substring(2, line.length() - 2);
	}
	
	public static String get_element(String line) {
		line = line.replaceAll("\\s+", ""); // remove space chars
//		line.replaceAll("\\(.*?\\)", ""); //remove (...)
		line = line.replaceAll("^#+", "");
		line = line.replaceAll("^\\*+", "");
		line = line.replaceAll("^#+", "");
		line = line.replaceAll("^\\*+", "");
		if (line.startsWith("{{")) {
			line = line.substring(line.indexOf('|')+1);
			if (line.indexOf('|') != -1)
				line = line.substring(0, line.indexOf('|'));
		}
		line = line.replaceAll("\\{.*\\}", "");
		line = line.replaceAll("<.*>", "");
		line = line.replaceAll("\\[\\[", "");
		line = line.replaceAll("\\]\\]", "");
		return line;
	}

	public static void fetch_ints_titles(String dir, String suffix_dict, String ofile) throws IOException {
		List<String> titles = new ArrayList<String>();

		// "/Users/zuoyuan/Documents/data/zhwiki/"
		File[] files = new File(dir).listFiles();
		for (File file : files) {
			BufferedReader reader = IOUtils.getReader(file.getAbsolutePath(), "utf-8");
			String line = reader.readLine();
			while (line != null) {
				if (line.startsWith("[[") && line.endsWith("]]")) {
					line = line.substring(2, line.length() - 2);
					titles.add(line.trim());
				}
				line = reader.readLine();
			}
			reader.close();
		}

		System.out.println("Number of titles: " + titles.size());

		Set<String> ins_suffix = new HashSet<String>();
		BufferedReader reader = IOUtils.getReader(suffix_dict, "utf-8");
		String line = reader.readLine();
		while (line != null) {
			ins_suffix.add(line.trim());
			line = reader.readLine();
		}
		reader.close();

		List<String> ins_titles = new ArrayList<String>();

		for (String title : titles) {
			boolean match = false;
			for (String ins_suf : ins_suffix) {
				if (title.endsWith(ins_suf)) {
					match = true;
					break;
				}
			}
			if (match) {
				ins_titles.add(title);
			}
		}

		System.out.println("Number of ins titles: " + ins_titles.size());

		BufferedWriter writer = IOUtils.getWriter(ofile, "utf-8");
		for (String it : ins_titles) {
			writer.write(it);
			writer.newLine();
		}
		writer.close();
	}

	public static void fetch_list_titles(String dir, String ofile) throws IOException {
		List<String> titles = new ArrayList<String>();

		// "/Users/zuoyuan/Documents/data/zhwiki/"
		File[] files = new File(dir).listFiles();
		for (File file : files) {
			BufferedReader reader = IOUtils.getReader(file.getAbsolutePath(), "utf-8");
			String line = reader.readLine();
			while (line != null) {
				if (line.startsWith("[[") && line.endsWith("]]")) {
					line = line.substring(2, line.length() - 2);
					titles.add(line.trim());
				}
				line = reader.readLine();
			}
			reader.close();
		}

		System.out.println("Number of titles: " + titles.size());

		List<String> list_titles = new ArrayList<String>();

		for (String title : titles) {
			boolean match = false;
			if (title.endsWith("列表")) {
				match = true;
			}
			if (match) {
				list_titles.add(title);
			}
		}

		BufferedWriter writer = IOUtils.getWriter(ofile, "utf-8");
		for (String lt : list_titles) {
			writer.write(lt);
			writer.newLine();
		}
		writer.close();
	}

	public static void fetch_ins(String dir, String suffix_dict, String ofile) throws IOException {
		String regex = "\\[\\[.*?\\]\\]";

		Pattern p = Pattern.compile(regex);

		Set<String> titles = new HashSet<String>();

		File[] files = new File(dir).listFiles();
		for (File file : files) {
			BufferedReader reader = IOUtils.getReader(file.getAbsolutePath(), "utf-8");
			String line = reader.readLine();
			while (line != null) {
				Matcher m = p.matcher(line.trim());
				while (m.find()) {
					String m_str = m.group();
					m_str = m_str.substring(2, m_str.length() - 2);
					if (m_str.indexOf('|') != -1) {
						m_str = m_str.substring(0, m_str.indexOf('|'));
					}
					titles.add(m_str.trim());
				}
				line = reader.readLine();
			}
			reader.close();
		}
		System.out.println("Number of titles: " + titles.size());

		Set<String> ins_suffix = new HashSet<String>();
		BufferedReader reader = IOUtils.getReader(suffix_dict, "utf-8");
		String line = reader.readLine();
		while (line != null) {
			ins_suffix.add(line.trim());
			line = reader.readLine();
		}
		reader.close();

		List<String> ins_titles = new ArrayList<String>();

		for (String title : titles) {
			boolean match = false;
			for (String ins_suf : ins_suffix) {
				if (title.endsWith(ins_suf)) {
					match = true;
					break;
				}
			}
			if (match) {
				ins_titles.add(title);
			}
		}

		System.out.println("Number of ins titles: " + ins_titles.size());

		BufferedWriter writer = IOUtils.getWriter(ofile, "utf-8");
		for (String it : ins_titles) {
			writer.write(it);
			writer.newLine();
		}
		writer.close();
	}
	
	public static void query_title(String dir, String title, int nlines) throws IOException {
		boolean print = false;
		int cnt = 0;
		
		File[] files = new File(dir).listFiles();
		for (File file : files) {
			BufferedReader reader = IOUtils.getReader(file.getAbsolutePath(), "utf-8");
			String line = reader.readLine();
			while (line != null) {
				if (line.startsWith("[[") && line.endsWith("]]") && line.equals("[["+title+"]]")) {
					print = true;
				}
				if (print) {
					System.out.println(line);
					cnt ++;
					if (cnt >= nlines) {
						System.exit(0);
					}
				}
				line = reader.readLine();
			}
			reader.close();
		}
	}
	
	
	public static void connected_ins(String dir, String ins_titles, String ins2ins_file) throws IOException {
		Set<String> ins_set = new HashSet<String>();
		BufferedReader reader = IOUtils.getReader(ins_titles, "utf-8");
		String line = reader.readLine();
		while (line != null) {
			ins_set.add(line.trim());
			line = reader.readLine();
		}
		reader.close();
		
		boolean is_ins = false, is_con = false;
		String ins_name = null;
		Map<String, List<String>> ins2ins = new HashMap<String, List<String>>();
		
		File[] files = new File(dir).listFiles();
		for (File file : files) {
			reader = IOUtils.getReader(file.getAbsolutePath(), "utf-8");
			line = reader.readLine();
			while (line != null) {
				if (is_con) {
					if (!ins2ins.containsKey(ins_name)) {
						ins2ins.put(ins_name, new ArrayList<String>());
					}
					if (RecogIns.is_section(line)) {
						is_con = false;
					}
					if (RecogIns.is_list_element(line)) {
						List<String> rel_ins = ins2ins.get(ins_name);
						rel_ins.add(RecogIns.get_element(line));
					}
				}
				if (is_ins) {
					if (RecogIns.is_section(line) && RecogIns.is_connected(line, ins_name)) {
						is_con = true;
					}
				}
				if (RecogIns.is_title(line)) {
					if (ins_set.contains(RecogIns.get_title(line))) {
						is_ins = true;
						ins_name = RecogIns.get_title(line);
					} else {
						is_ins = false;
					}
				}
				line = reader.readLine();
			}
			reader.close();
		}
		
		System.out.println(ins2ins.size());
		
		BufferedWriter writer = IOUtils.getWriter(ins2ins_file, "utf-8");
		for (String ins : ins2ins.keySet()) {
			writer.write("[["+ins+"]]");
			writer.newLine();
			for (String r_ins : ins2ins.get(ins)) {
				writer.write("* "+r_ins);
				writer.newLine();
			}
		}
		writer.close();
	}
	

	public static void main(String args[]) throws IOException {
//		RecogIns.fetch_ins("/Users/zuoyuan/Documents/data/zhwiki/", "ins_dict.txt", "ins_titles_all.txt");
//		RecogIns.query_title("/Users/zuoyuan/Documents/data/zhwiki/", "加拿大音乐协会", 200);
//		System.out.println("##sad".replaceAll("^#+", ""));
		RecogIns.connected_ins("/Users/zuoyuan/Documents/data/zhwiki/", "ins_titles.txt", "ins2ins.txt");
	}
}

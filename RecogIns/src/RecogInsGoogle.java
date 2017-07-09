

import java.io.BufferedReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.dictionary.CustomDictionary;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.CRF.CRFSegment;
import com.hankcs.hanlp.seg.NShort.NShortSegment;
import com.hankcs.hanlp.seg.common.Term;
import com.hankcs.hanlp.tokenizer.NLPTokenizer;

public class RecogInsGoogle {

	public static int span = 5;
	
	public static int left_span = 3;
	
	public static int right_span = 9;
	
	public static boolean insert = false;
	
	public static boolean check_prev = false;
	
	public static boolean check_next = false;
	
	public static Map<String, Set<String>> get_sents(String file, String[] targets) throws IOException {
		Map<String, Set<String>> pat2sents = new HashMap<String, Set<String>>();

		BufferedReader reader = IOUtils.getReader(file, "utf-8");

		String line = reader.readLine();
		while (line != null) {
			String abs = line.split("\\|text\\|")[2].replaceAll("\\.\\.\\.", "");
			String pat = line.split("\\|text\\|")[4].replaceAll("\\.\\.\\.", "");

			if (!pat2sents.containsKey(pat)) {
				pat2sents.put(pat, new HashSet<String>());
			}
			abs = abs.substring(abs.indexOf("网页快照") + "网页快照".length());
			abs = HanLP.convertToSimplifiedChinese(abs);
			String[] sents = abs.split("[,，。-]");
			for (String sent : sents) {
				for (String target : targets) {
					if (sent.contains(target)) {
						pat2sents.get(pat).add(sent.trim());
//						System.out.println(NLPTokenizer.segment(sent.trim()));
						pat2sents.put(pat, pat2sents.get(pat));
					}
				}
			}
			line = reader.readLine();
		}

//		System.out.println(tmp);
		// for (String pat : pat2sents.keySet()) {
		// System.out.println(pat);
		// for (String sent : pat2sents.get(pat)) {
		// System.out.println(sent);
		// }
		// System.out.println("------------------------");
		// System.out.println();
		// System.out.println();
		// System.out.println();
		// }

		return pat2sents;
	}

	public static boolean contain_target(String str, String[] targets) {
		for (String target : targets) {
			if (str.contains(target)) {
				return true;
			}
		}
		return false;
	}

	public static List<Term> merge_nt_cc_nt(List<Term> cur_terms) {
		for (int i = 0; i != cur_terms.size(); i++) {
			if (cur_terms.get(i).nature.toString().startsWith("nt") && i + 2 < cur_terms.size()) {
				if (cur_terms.get(i + 1).nature.toString().compareTo("cc") == 0
						&& cur_terms.get(i).nature.toString().startsWith("nt")) {
					String word = cur_terms.get(i).word + cur_terms.get(i + 1).word + cur_terms.get(i + 2).word;
					cur_terms.remove(i + 1);
					cur_terms.remove(i + 1);
					cur_terms.get(i).word = word;
				}
			}
		}
		return cur_terms;
	}

	// 是/vshi 的/ude1
	public static Set<String> fetch_related_ins_1(Set<String> sent_set, String[] targets, Set<String> candidates,
			boolean insert, boolean check_prev, boolean check_next) {
		if (insert) {
			for (String target : targets)
				CustomDictionary.insert(target, "nt 4096");
		}
		for (String sent : sent_set) {
			List<Term> termList = NLPTokenizer.segment(sent);
//			termList = merge_nt_cc_nt(termList);
//			Segment segment = new NShortSegment().enableCustomDictionary(false).enablePlaceRecognize(true).enableOrganizationRecognize(true);
//			Segment segment = new CRFSegment();
//			segment.enablePartOfSpeechTagging(true).enableOrganizationRecognize(true);
//			Segment segment = HanLP.newSegment().enableOrganizationRecognize(true);
//			List<Term> termList = segment.seg(sent);
			for (int i = 0; i != termList.size(); i++) {
				Term curr_term = termList.get(i);
				Term prev_term = null;
				if (i - 1 >= 0) {
					prev_term = termList.get(i - 1);
				}
				if ((curr_term.word.contains("所属") || curr_term.word.contains("下属")
						|| curr_term.word.contains("直属"))) {
//				if ((curr_term.word.compareTo("所属") == 0 || curr_term.word.compareTo("下属") == 0
//						|| curr_term.word.compareTo("直属") == 0)) {
					if (check_prev) {
						if (prev_term != null && contain_target(prev_term.word, targets)) {
							boolean enter = false;
							int e = i + span >= termList.size() ? termList.size() : i + span + 1;
							for (int b = i + 1; b != e; b++) {
								if (termList.get(b).nature.toString().startsWith("nt") && termList.get(b).word.length() > 2) {
									enter = true;
									candidates.add(termList.get(b).word);
								}
							}
//							if (enter) {
//								System.out.println(termList);
//							}
						}
					} else {
						boolean enter = false;
						int e = i + span >= termList.size() ? termList.size() : i + span + 1;
						for (int b = i + 1; b != e; b++) {
							if (termList.get(b).nature.toString().startsWith("nt") && termList.get(b).word.length() > 2) {
								enter = true;
								candidates.add(termList.get(b).word);
							}
						}
//						if (enter) {
//							System.out.println(termList);
//						}
					}
				}
			}
			for (int i = 0; i != termList.size(); i++) {
				Term curr_term = termList.get(i);
				Term next_term = null;
				if (i + 1 < termList.size())
					next_term = termList.get(i + 1);
				if (curr_term.nature.toString().compareTo("vshi") == 0) {
					if (check_next && next_term != null && contain_target(next_term.word, targets)) {
						boolean enter = false;
						for (int b = i - span < 0 ? 0 : i - span; b != i; b++) {
							if (termList.get(b).nature.toString().startsWith("nt") && termList.get(b).word.length() > 2) {
								enter = true;
								candidates.add(termList.get(b).word);
							}
						}
//						if (enter) {
//							System.out.println(termList);
//						}
					} else {
						boolean enter = false;
						for (int b = i - span < 0 ? 0 : i - span; b != i; b++) {
							if (termList.get(b).nature.toString().startsWith("nt")) {
								enter = true;
								candidates.add(termList.get(b).word);
							}
						}
//						if (enter) {
//							System.out.println(termList);
//						}
					}
				}
			}
		}
		return candidates;
	}
	
	public static Set<String> fetch_related_ins_2(Set<String> sent_set, String[] targets, Set<String> candidates,
			boolean insert, int left_span, int right_span) {
		if (insert) {
			for (String target : targets)
				CustomDictionary.insert(target, "nt 4096");
		}
		
		for (String sent : sent_set) {
			List<Term> termList = NLPTokenizer.segment(sent);
			termList = merge_nt_cc_nt(termList);
			boolean enter = false;
			for (int i = 0; i != termList.size(); i++) {
				Term curr_term = termList.get(i);
				if (contain_target(curr_term.word, targets)) {
					//search left
					for (int b = i - left_span < 0 ? 0 : i - left_span; b != i; b++) {
						if (termList.get(b).nature.toString().startsWith("nt")) {
							enter = true;
							candidates.add(termList.get(b).word);
						}
					}
					
					//search right
					int e = i + right_span > termList.size() ? termList.size() : i + right_span; 
					for (int b = i + 1; b != e; b++) {
						if (termList.get(b).nature.toString().startsWith("nt")) {
							enter = true;
							candidates.add(termList.get(b).word);
						}
					}
				}
			}
//			if (enter) System.out.println(termList);
		}
		return candidates;
	}
	
	public static Set<String> fetch_related_ins_3(Set<String> sent_set, String[] targets, String[] suffixs, Set<String> candidates,
			boolean insert) {
		if (insert) {
			for (String target : targets)
				CustomDictionary.insert(target, "nt 4096");
		}
		for (String sent : sent_set) {
			for (String target : targets) {
				for (String suffix : suffixs) {
					int b = sent.indexOf(target);
					int e = sent.indexOf(suffix);
					if (b != -1 && e != -1 && b < e && e-(b+target.length()) <= 10) {
						if (e + suffix.length() < sent.length() && sent.charAt(e + suffix.length()) != '长')  {
							String candidate = sent.substring(b+target.length(), e+suffix.length()).replaceAll("[.。”） ]", "");
//							String candidate = sent.substring(b, e+suffix.length());
							if (!candidate.contains(",") && !candidate.contains("，") 
									&& !candidate.contains("：") && !candidate.contains(":")
									&& !candidate.contains("《") && !candidate.contains("“")
									&& !candidate.contains("\"") && !candidate.contains("、") && candidate.length() > 2) {
								candidates.add(candidate);
							}
						}
					}
				}
			}
		}
		return candidates;
	}

//	public static void main(String args[]) throws IOException {
////		String google_data = "/Users/zuoyuan/Desktop/islamstate_search_results.txt";
////		String google_data = "/Users/zuoyuan/Desktop/fagaiwei_search_results.txt";
//		String google_data = "/Users/zuoyuan/Desktop/jiagesi_search_results.txt";
////		String[] targets = new String[] { "发改委", "国家发改委", "国家发展和改革委员会" };
////		String[] targets = new String[]{"伊斯兰", "伊斯兰国"};
//		String[] targets = new String[]{"价格司"};
//		String[] suffixs = new String[]{"处"};
//		Map<String, Set<String>> pat2sents = get_sents(google_data, targets);
//		Set<String> candidates = new HashSet<String>();
//		for (String pat : pat2sents.keySet()) {
//			if (pat.contains("所属") || pat.contains("下属") || pat.contains("直属")) {
//				if (span != -1) {
//					fetch_related_ins_1(pat2sents.get(pat), targets, candidates, insert, check_prev, check_next);
//				}
//			} 
//			if (pat.contains("效忠")) {
//				if (left_span != -1 || right_span != -1) {
//					fetch_related_ins_2(pat2sents.get(pat), targets, candidates, insert, left_span, right_span);
//				}
//			}
//			if (pat.contains("处")) {
//				fetch_related_ins_3(pat2sents.get(pat), targets, suffixs, candidates, insert);
//			}
//		}
//		for (String cand : candidates) {
//			System.out.println(cand);
//		}
//	}
	
	public static void main(String args[]) throws IOException {
		if (args.length < 6) {
			System.out.println("Need more parameters to run!");
			System.exit(-1);
		}
		String google_data = args[0];
		String[] targets = args[1].split(",");
		String[] suffixs = null;
		if (args[2].compareTo("None") != 0) {
			suffixs = args[2].split(",");
		}
		span = Integer.valueOf(args[3]);
		left_span = Integer.valueOf(args[4]);
		right_span = Integer.valueOf(args[5]);
		Map<String, Set<String>> pat2sents = get_sents(google_data, targets);
		Set<String> candidates = new HashSet<String>();
		for (String pat : pat2sents.keySet()) {
			if (pat.contains("所属") || pat.contains("下属") || pat.contains("直属")) {
				if (span != -1) {
					fetch_related_ins_1(pat2sents.get(pat), targets, candidates, insert, check_prev, check_next);
				}
			} 
			if (pat.contains("效忠")) {
				if (left_span != -1 || right_span != -1) {
					fetch_related_ins_2(pat2sents.get(pat), targets, candidates, insert, left_span, right_span);
				}
			}
			if (pat.contains("处") || pat.contains("司")) {
				fetch_related_ins_3(pat2sents.get(pat), targets, suffixs, candidates, insert);
			}
		}
		System.out.println("#"+targets[0]);
		for (String cand : candidates) {
			System.out.println(cand);
		}
	}
}

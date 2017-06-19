package com.hankcs.ml;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;

public class IOUtils {
	public static BufferedReader getReader(String path, String charset) {
		BufferedReader reader = null;
		try {
			reader = new BufferedReader(new InputStreamReader(new FileInputStream(path), charset));
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return reader;
	}

	public static BufferedWriter getWriter(String path, String charset) {
		BufferedWriter writer = null;
		try {
			writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path), charset));
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return writer;
	}

	public static void writeObject(String path, Object map) throws IOException {
		File f = new File(path);
		FileOutputStream out = new FileOutputStream(f);
		ObjectOutputStream objwrite = new ObjectOutputStream(out);
		objwrite.writeObject(map);
		objwrite.flush();
		objwrite.close();
	}

	// read the object from the file
	public static Object readObject(String path) throws IOException, ClassNotFoundException {
		FileInputStream in = new FileInputStream(path);
		ObjectInputStream objread = new ObjectInputStream(in);
		Object map = objread.readObject();
		objread.close();
		return map;
	}

}
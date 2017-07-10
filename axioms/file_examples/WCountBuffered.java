import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;

import java.io.BufferedReader;
import java.io.BufferedWriter;

import java.io.FileNotFoundException;
import java.io.IOException;

import java.util.Set;
import java.util.Map;
import java.util.HashMap;

class WCountBuffered {
    public static void main(String[] args) {
	Map<String, Integer> counts = new HashMap<>();
	BufferedReader in;
	BufferedWriter out;
	try {
	    in = new BufferedReader(new FileReader(args[0]));
	    try {
		out = new BufferedWriter(new FileWriter("counts" + "_" + args[0]));
		String line = in.readLine();
		while (line != null) {
		    String[] words = line.split(" ");
		    for (String word : words) {
			if (counts.containsKey(word)) {
			    counts.replace(word, counts.get(word) + 1);
			}
			else {
			    counts.put(word, 1);
			}
		    }
		    line = in.readLine();
		}
		for (String k : counts.keySet()) {
		    out.write(k + "," + counts.get(k));
		    out.newLine();
		}
		out.close();
	    } catch (IOException e) {
		System.out.println("IOException out: " + e);
	    }
	    try {
		in.close();
	    } catch(IOException e) {
		System.out.println("IOException in: " + e);
	    }
	} catch (FileNotFoundException e) {
	    System.out.println("File not found: " + e);
	}
    }
}

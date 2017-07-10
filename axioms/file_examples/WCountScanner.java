import java.io.File;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.IOException;

import java.util.Map;
import java.util.HashMap;
import java.util.Scanner;

class WCountScanner {
    public static void main(String[] args) {
	Map<String, Integer> counts = new HashMap<>();
	BufferedWriter out;
	Scanner s;
	try {
	    s = new Scanner(new File(args[0]));
	    while (s.hasNext()) {
		String word = s.next();
		if (counts.containsKey(word)) counts.replace(word, counts.get(word) + 1);
		else counts.put(word, 1);
	    }
	    try {
		out = new BufferedWriter(new FileWriter("counts" + "_" + args[0]));
		for (String k : counts.keySet()) {
		    out.write(k + "," + counts.get(k));
		    out.newLine();
		}
		out.close();
	    } catch (IOException e) {
		System.out.println("IOException: " + e);
	    }
	} catch(FileNotFoundException e) {
	    System.out.println("File not found: " + e);
	}
    }
}

import java.io.File;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.IOException;

import java.util.Map;
import java.util.HashMap;
import java.util.Scanner;

class WCountScanner {
    harness void main() {
	Map<String, Integer> counts = new HashMap_Simple<>();
	BufferedWriter out;
	Scanner s;
	s = new Scanner(new File("file.txt"));
	while (s.hasNext()) {
	    String word = s.next();
	    int i = counts.get(word).intValue() + 1;
	    if (counts.containsKey(word)) counts.replace(word, new Integer(i));
	    else counts.put(word, new Integer(1));
	}
	out = new BufferedWriter(new FileWriterr("counts_file.txt"));
	// for (String k : counts.keySet()) {
	//     out.write(k + "," + counts.get(k));
	//     out.newLine();
	// }
	// out.close();
	// 	try {
    // 	    s = new Scanner(new File(args[0]));
    // 	    while (s.hasNext()) {
    // 	    	String word = s.next();
    // 	    	if (counts.containsKey(word)) counts.replace(word, counts.get(word) + 1);
    // 	    	else counts.put(word, 1);
    // 	    }
    // 	    try {
    // 	    	out = new BufferedWriter(new FileWriter("counts" + "_" + args[0]));
    // 	    	for (String k : counts.keySet()) {
    // 	    	    out.write(k + "," + counts.get(k));
    // 	    	    out.newLine();
    // 	    	}
    // 	    	out.close();
    // 	    } catch (IOException e) {
    // 	    	System.out.println("IOException: " + e);
    // 	    }
    // 	} catch(FileNotFoundException e) {
    // 	    System.out.println("File not found: " + e);
    // 	}
    }
}

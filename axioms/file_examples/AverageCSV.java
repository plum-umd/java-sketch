import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.BufferedWriter;

import java.io.IOException;
import java.io.FileNotFoundException;

import java.util.ArrayList;
import java.util.Scanner;

class AverageCSV {
    public static void main(String[] args) {
	BufferedWriter out;
	Scanner s;
	try {
	    s = new Scanner(new File(args[0]));
	    try {
		out = new BufferedWriter(new FileWriter("avgs" + "_" + args[0]));
		while(s.hasNextLine()) {
		    float tot = 0;
		    String line = s.nextLine();
		    String[] splits = line.split(",");
		    for (String n : splits) tot += Float.parseFloat(n);
		    tot /= splits.length;
		    out.write(new Float(tot).toString());
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

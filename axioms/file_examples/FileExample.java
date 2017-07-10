//https://www.tutorialspoint.com/javaexamples/java_files.htm

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;

public class FileExample {
    public static void main(String[] args) {
	try {
	    BufferedReader in = new BufferedReader(new FileReader(args[0]));
	    File file = new File("copy_"+args[0]);
	    FileWriter fw = new FileWriter(file.getAbsoluteFile());
	    BufferedWriter bw = new BufferedWriter(fw);
	    if (!file.exists()) {
		file.createNewFile();
	    }
	    String str = in.readLine();
	    while (str != null) {
		bw.write(str);
		bw.newLine();
		str = in.readLine();
	    }
	    bw.close();
	    System.out.println("Done");
	} catch (IOException e) {
	    e.printStackTrace();
	}
    }
}

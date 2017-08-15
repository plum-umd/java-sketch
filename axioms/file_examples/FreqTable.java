//https://www.cs.utexas.edu/~scottm/cs307/javacode/codeSamples/FreqTableExampleOriginal.java
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.util.Map;
import java.util.HashMap;

public class FreqTable {
    public static final int NUM_ASCII_CHAR = 128;
    public static final String file0;

    // Original program modified to remove print statements, some catch blocks, and URL frequency table
    public static harness void main() {
	Map<Character, Integer> freqs = new HashMap_NoHash<>();
	String file0_d = "a";
	String file0_n = "f";
	freqs = createTable(file0_n, file0_d);
	// if (freqs.size() == 0) assert false;
	Character c = new Character('a');
	Integer i = freqs.get(c);
	assert i.intValue() == 0;
	// else {
	//     assert freqs[97] == 1;
	//     for(int i = 0; i < freqs.length; i++) {
	// 	assert freqs[i] == file0.charAt(i);
	// // 	System.out.println("charcater code: " + i + " ,character: " + (char)i + " ,frequency: " + freqs[i]);
	//     System.out.println("Total characters in file: " + sum(freqs));
	// }
	// assert true;
    }
    // private static int sum(Integer[] list) {
    // 	assert list != null : "Failed precondition, sum: parameter list may not be null.";
    // 	// changed total from int to Integer, don't support boxing yet
    // 	Integer total = new Integer(0);
    // 	for(Integer x : list){
    // 	    total.value += x.intValue();
    // 	}
    // 	return total.intValue();
    // }
    public static HashMap<Character, Integer> createTable(String fileName, String data) throws FileNotFoundException, IOException{
    	Map<Character, Integer> freqs = new HashMap_NoHash<>();
    	File f = new File(fileName);
    	FileReaderr r = new FileReaderr(f);
    	while (r.ready()) {
    	    Character ch = new Character(r.read());
    	    Integer i = freqs.get(ch);
    	    if (i != null) {
		assert ch.charValue() == 'b';
    		freqs.replace(ch, new Integer(i.intValue() + 1));
    	    }
    	    else {
		assert ch.charValue() == 'b';
    		freqs.put(ch, new Integer(1));
    	    }
    	}
    	r.close();
    	return freqs;
    }
}

/* ORIGINAL PROGRAM */
// import java.io.File;
// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;
// import java.io.InputStreamReader;
// import java.io.FileInputStream;

// public class FreqTable {
//     public static final int NUM_ASCII_CHAR = 128;

//     // program to create a frequency table.
//     // Example of simple try catch blocks to deal with checked exceptions
//     public static void main(String[] args)
//     {
// 	int[] freqs = createFreqTableURL(args[0]);
// 	if( freqs.length == 0)
// 	    System.out.println("No frequency table created due to problems when reading from file");
// 	else{
// 	    for(int i = 0; i < NUM_ASCII_CHAR; i++){
// 		System.out.println("charcater code: " + i + " ,character: " + (char)i + " ,frequency: " + freqs[i]);
// 	    }
// 	    System.out.println("Total characters in file: " + sum(freqs));
// 	}


// 	int[] freqs = new int[]{};
// 	try{
// 	    freqs = createTable(args[0]);
// 	}
// 	catch(FileNotFoundException e){
// 	    System.out.println("File not found. Unable to create freq table" + e);
// 	}
// 	catch(IOException e){
// 	    System.out.println("Problem while reading from file. Unable to create freq table" + e);
// 	}
// 	if( freqs.length == 0)
// 	    System.out.println("No frequency table created due to problems when reading from file");
// 	else{
// 	    for(int i = 0; i < freqs.length; i++){
// 		System.out.println("charcater code: " + i + " ,character: " + (char)i + " ,frequency: " + freqs[i]);
// 	    }
// 	    System.out.println("Total characters in file: " + sum(freqs));
// 	}

//     }


//     // return sum of ints in list
//     // list may not be null
//     private static int sum(int[] list) {
// 	assert list != null : "Failed precondition, sum: parameter list" +
// 	    " may not be null.";
// 	int total = 0;
// 	for(int x : list){
// 	    total += x;
// 	}
// 	return total;
//     }


//     // pre: url != null
//     // Connect to the URL specified by the String url.
//     // Map characters to index in array.
//     // All non ASCII character dumped into one element of array
//     // If IOException occurs message printed and array of
//     // length 0 returned.
//     public static int[] createFreqTableURL (String url){
// 	if(url == null)
// 	    throw new IllegalArgumentException("Violation of precondition. parameter url must not be null.");

// 	int[] freqs = new int[NUM_ASCII_CHAR];
// 	try {
// 	    InputStreamReader in = new InputStreamReader(new FileInputStream(url));
// 	    while(in.ready()){
// 		int c = in.read();
// 		if(0 <= c && c < freqs.length)
// 		    freqs[c]++;
// 		else
// 		    System.out.println("Non ASCII char: " + c + " " + (char) c);
// 	    }
// 	    in.close();
// 	}
// 	catch(IOException e){
// 	    System.out.println("Unable to read from resource." + e);
// 	    freqs = new int[0];
// 	}
// 	return freqs;
//     }
//     // Connect to the file specified by the String fileName.
//     // Assumes it is in same directory as compiled code.
//     // Map characters to index in array.
//     public static int[] createTable(String fileName) throws FileNotFoundException, IOException{
// 	int[] freqs = new int[NUM_ASCII_CHAR];
// 	File f = new File(fileName);
// 	FileReader r = new FileReader(f);
// 	while( r.ready() ){
// 	    int ch = r.read();
// 	    if(0 <= ch && ch < freqs.length)
// 		freqs[ch]++;
// 	    else
// 		System.out.println((char) ch);
// 	}
// 	r.close();
// 	return freqs;
//     }
// }

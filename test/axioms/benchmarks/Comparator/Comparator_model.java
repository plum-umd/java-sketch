import java.io.IOException;
import java.util.ArrayList;

public class Comparator {

	// public static void main(String[] args) {
	// public static void main() {
	harness public void main() {
		
	    CommunicationWithFiles communication = new CommunicationWithFiles();
	    String File1="1\n2";
	    String File2="2\n3";
	    
	    ArrayList<String> inFile1 = new ArrayList<String>();
	    ArrayList<String> inFile2 = new ArrayList<String>();
	    inFile1 = communication.ReadToArray(File1, false);
	    inFile2 = communication.ReadToArray(File2, false); 
	    inFile1.addAll(inFile2);

	    String o1 = File1.concat("_vs_");
	    String o2 = o1.concat(File2);
	    String outputFileName = o2.concat(".txt");
	    ArrayList<String> comp = communication.RemoveDuplicates(inFile1);

	    String c1 = comp.get(1);
	    String c2 = comp.get(2);

	    assert c1.equals("1|1\n2");
	    assert c2.equals("3|2\n3");
	    
	    assert comp.size() == 3;

	    // File1 = "3\n4\n5";
	    // File2 = "4\n5\n6";

	    // inFile1 = communication.ReadToArray(File1, false);
	    // inFile2 = communication.ReadToArray(File2, false); 
	    // inFile1.addAll(inFile2);

	    // comp = communication.RemoveDuplicates(inFile1);

	    // c1 = comp.get(1);
	    // c2 = comp.get(2);

	    // assert c1.equals("3|3\n4\n5");
	    // assert c2.equals("6|4\n5\n6");
	    
	    // assert comp.size() == 3;

	}

}



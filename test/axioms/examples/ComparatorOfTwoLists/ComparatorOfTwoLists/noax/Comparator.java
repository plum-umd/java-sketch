import java.io.IOException;
import java.util.ArrayList;

public class Comparator {

	public static void main(String[] args) {
		
	    // if(args.length==2) {		
	    CommunicationWithFiles communication = new CommunicationWithFiles();
	    // String File1=args[0];
	    // String File2=args[1];
	    String File1="f1.txt";
	    String File2="f2.txt";

	    ArrayList<String> inFile1 = new ArrayList<String>();
	    ArrayList<String> inFile2 = new ArrayList<String>();
	    // try {
	    inFile1 = communication.ReadToArray(File1, false);
	    // System.out.println("File 1 was loaded"+"\n");
	    inFile2 = communication.ReadToArray(File2, false); 
	    // System.out.println("File 2 was loaded"+"\n");
	    inFile1.addAll(inFile2);

	    // // } catch (IOException e) {
	    // //     // TODO Auto-generated catch block
	    // //     e.printStackTrace();
	    // // }

	    // // try {
	    String o1 = File1.concat("_vs_");
	    String o2 = o1.concat(File2);
	    String outputFileName = o2.concat(".txt");
	    // String outputFileName=File1+"_vs_"+File2+".txt";
	    communication.createFile(communication.RemoveDuplicates(inFile1),outputFileName);

	    // } catch (IOException e) {
	    //     // TODO Auto-generated catch block
	    //     e.printStackTrace();
	    // }



	    // }else {
	    // 	// System.out.println("Incorrect number of attributes.");
	    // }
	    
	}

}



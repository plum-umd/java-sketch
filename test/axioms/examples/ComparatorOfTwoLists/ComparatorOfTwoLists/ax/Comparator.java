import java.io.IOException;
import java.util.ArrayList;

public class Comparator {

	public static void main(String[] args) {
		
		if(args.length==2) {
		 CommunicationWithFiles communication = new CommunicationWithFiles();
		 String File1=args[0];
		 String File2=args[1];
		 
         ArrayList<String> inFile1 = new ArrayList<String>();
         ArrayList<String> inFile2 = new ArrayList<String>();
         try {
             inFile1 = communication.ReadToArray(File1, false);
             System.out.println("File 1 was loaded"+"\n");
             inFile2 = communication.ReadToArray(File2, false); 
             System.out.println("File 2 was loaded"+"\n");
             inFile1.addAll(inFile2);
            
         } catch (IOException e) {
             // TODO Auto-generated catch block
             e.printStackTrace();
         }
         
         try {
        	 String outputFileName=File1+"_vs_"+File2+".txt";
            communication.createFile(communication.RemoveDuplicates(inFile1),outputFileName);
            
         } catch (IOException e) {
             // TODO Auto-generated catch block
             e.printStackTrace();
         }
		}else {
			System.out.println("Incorrect number of attributes.");
		}
		
	}

}



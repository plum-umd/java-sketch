import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

public class CommunicationWithFiles {

    
    public CommunicationWithFiles(){};

    generator public String genRead(BufferedReader bfr, String value, boolean isAList, ArrayList<> values, String filename) {
	// String vbar = null;
	// if (??) {
	//     value = bfr.readLine();
	//     while(value != null){  
	// 	if (value!=null && !isAList==true){
	// 	    // values.add(value+"|"+filename);
	// 	    String vbar = value.concat("|");
	// 	    values.add(vbar.concat(filename));
	// 	}
	// 	value = bfr.readLine();
	//     }
	// }

	// if (??) {
	//     value = bfr.readLine();
	//     while(value != null){  
	//         value = genRead(bfr, value, isAList, values, filename);		
	//     }
	// }
	// if (??) {
	//     if (value!=null && !isAList==true){
	// 	// values.add(value+"|"+filename);
	// 	String vbar = value.concat("|");
	// 	values.add(vbar.concat(filename));
	//     }
	//     value = bfr.readLine();
	// }

	if (??) {
	    if (value!=null && !isAList==true){
		// values.add(value+"|"+filename);
		String vbar = value.concat("|");
		values.add(vbar.concat(filename));
	    }
	}	
	if (??) {
	    value = bfr.readLine();
	}
	if (??) {
	    while(value != null){  
	        value = genRead(bfr, value, isAList, values, filename);
	    }
	}
	// if (??) {
	//     value = genRead(bfr, value, isAList, values, filename);
	// }
	
	// if (??) {
	//     value = bfr.readLine();
	// }
	// // if (??) {
	// //     while(value != null) {
	// // 	genRead(bfr, value, isAList, values, filename);
	// //     }
	// // }
	// // if (??) {
	// //     if (value != null && !isAList == true) {
	// // 	genRead(bfr, value, isAList, values, filename);
	// //     }
	// // }
	// if (??) {
	//     vbar = value.concat("|");
	//     vbar = vbar.concat(filename);
	// }
	// if (??) {
	//     if (value != null && !isAList == true) {	    
	// 	values.add(vbar);
	//     }
	// }

	return value;
    }

        /**
         * Function is creating diff.txt file
         * @param  arg filename name of the file to be loaded
         * @param  arg true for list of values
         */
        public ArrayList<String> ReadToArray(String filename,boolean isAList ) throws IOException{    
    
                FileReaderr fr = null;
                String value = "";
                
                ArrayList<String> values = new ArrayList<String>();
                Collections.sort(values);
                    // try {
		fr = new FileReaderr(filename);
                        // } catch (FileNotFoundException e1) {
                        //         System.out.println("Error opening the file (file not found)");
                        //         //     System.exit(1);
                        //     }
		BufferedReader bfr = new BufferedReader(fr);
                            // try {

		genRead(bfr, value, isAList, values, filename);
		
		// value = bfr.readLine();
		// // while(value != null){  
		// //     if (value!=null && !isAList==true){
		// // 	// values.add(value+"|"+filename);
		// // 	String vbar = value.concat("|");
		// // 	values.add(vbar.concat(filename));
		// //     }
		// //     value = bfr.readLine();
		// // }
		// while(value != null){  
		//     // if (value!=null && !isAList==true){
		//     // 	// values.add(value+"|"+filename);
		//     // 	String vbar = value.concat("|");
		//     // 	values.add(vbar.concat(filename));
		//     // }
		//     // value = bfr.readLine();
		//     genRead(bfr, value, isAList, values, filename);
		// }
                                // } catch (IOException e) {
                                //         System.out.println("Error reading the file");
                                //             System.exit(2);
                                //     }

                                // try {
		fr.close();
                                    // } catch (IOException e11) {
                                    //     System.out.println("Error closing the file");
                                    //     System.exit(3);
                                    //     }
		return values;    
                } 
                               
        /**
         * Function is removing duplicated lines from ArrayList<String>
         * @param  toBeSorted - array to be sorted
         * @return ArrayList<String> without duplicated lines
         */
        public ArrayList<String> RemoveDuplicates(ArrayList<String> toBeSorted){
            int j=1;

            toBeSorted.sort(null);

	    while(j+1<toBeSorted.size()){
		String get_j = toBeSorted.get(j);
		String sstr = get_j.substring(0, get_j.indexOf("|"));
		String get_j1 = toBeSorted.get(j+1);
		String sstr1 = get_j1.substring(0, get_j1.indexOf("|"));
		if (sstr.equals(sstr1)) {
            //     if( toBeSorted.get(j).substring(0,toBeSorted.get(j).indexOf("|")).equals(toBeSorted.get(j+1).substring(0,toBeSorted.get(j+1).indexOf("|")) )){
                	toBeSorted.remove(j+1);
                        toBeSorted.remove(j);
                }else{j++; 	}
            }   
            toBeSorted.add(0, "Values present in only one file|File name");
            return toBeSorted;
        }   

        /**
         * Function is creating diff.txt pipe delimited file.
         * @param  rows with values to be checked
         */
        public void createFile(ArrayList<String> rows, String filename) throws IOException{
    
            FileWriterr fileWriter = new FileWriterr(filename);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter); 

            // try{
	    for(int k=0;k<= rows.size()-1;k++){
		String v = rows.get(k);
		bufferedWriter.write(v);
		bufferedWriter.newLine();
	    }
            // }finally{
	    bufferedWriter.close();
	    // System.out.println(filename+" was created");
            // }
        }

        /**
         * Function is clearing chosen file
         * @param  name of the file to be cleared
         */
        public void ClearFile(String toBeCleared) throws IOException{
            FileWriterr fileWriter = new FileWriterr(toBeCleared);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter); 
            
            bufferedWriter.close();
            

        }   
        
        
}

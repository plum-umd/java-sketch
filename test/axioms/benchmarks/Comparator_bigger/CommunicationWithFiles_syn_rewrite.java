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
	    if (value!=?? && !isAList==true){
		// // values.add(value+"|"+filename);
		// char[] c = new char[1];
		// c[0] = ??;
		// String bar = new String(c, 0, 1);
		String vbar = value.concat("|");
		// String vbar = value.concat(bar);
		values.add(vbar.concat(filename));

		// // values.add(value+"|"+filename);
		// String vbar = value.concat("|");
		// values.add(vbar.concat(filename));
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
	if (??) {
	    value = genRead(bfr, value, isAList, values, filename);
	}
	
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
    
	    // FileReaderr fr = null;
	    // String value = null;
	    boolean[] localBools = new boolean[1];
	    localBools[0] = isAList;
	    Object[] localObjs = new Object[6];
	    localObjs[0] = filename;

	    localObjs[1] = null;
	    localObjs[2] = new ArrayList<String>();

	    ArrayList<String> values = (ArrayList<String>) localObjs[2];
	    values.sort(null);
	    String fname = (String) localObjs[0];
	    localObjs[3] = new FileReaderr(fname);
	    FileReaderr fr = (FileReaderr) localObjs[3];
	    localObjs[4] = new BufferedReader(fr);
		
	    // ArrayList<String> values = new ArrayList<String>();
	    // values.sort(null);
	    // fr = new FileReaderr(filename);
	    // BufferedReader bfr = new BufferedReader(fr);

	    BufferedReader br = (BufferedReader) localObjs[4];
	    localObjs[1] = br.readLine();

	    while(localObjs[1] != null) {		
		if (localObjs[1] != null && !localBools[0] == true){
		    String value = (String) localObjs[1];
		    localObjs[5] = value.concat("|");
		    String vbar = (String) localObjs[5];
		    ArrayList<String> values2 = (ArrayList<String>) localObjs[2];
		    String fname2 = (String) localObjs[0];
		    values2.add(vbar.concat(fname2));
		}
		BufferedReader br2 = (BufferedReader) localObjs[4];
		localObjs[1] = br2.readLine();		
	    }	    

	    FileReaderr fr2 = (FileReaderr) localObjs[3];
	    fr2.close();
	    ArrayList<String> values3 = (ArrayList<String>) localObjs[2];
	    return values3;
	    // fr.close();
	    // return values;    
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
            // toBeSorted.add(0, "Values present in only one file|File name");
            toBeSorted.set(0, "V|F");
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

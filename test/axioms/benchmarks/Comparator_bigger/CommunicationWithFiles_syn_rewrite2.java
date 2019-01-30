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


    generator ArrayList<String> genArrayList(boolean[] localBools, Object[] localObjs) {
	if (??) { return new ArrayList<String>(); }
	if (??) { return localObjs[2]; }
	return null;
    }

    generator String genString(boolean[] localBools, Object[] localObjs) {
	if (??) { return localObjs[0]; }
	if (??) { return localObjs[1]; }
	if (??) { return localObjs[5]; }
	if (??) {
	    BufferedReader br = genBufferedReader(localBools, localObjs);
	    return br.readLine();
	}
	if (??) {
	    String value = genString(localBools, localObjs);
	    return value.concat("|");

	}
	return null;
    }
    
    generator BufferedReader genBufferedReader(boolean[] localBools, Object[] localObjs) {
	if (??) { return localObjs[4]; }
	if (??) {
	    FileReaderr fr = genFileReaderr(localBools, localObjs);
	    return new BufferedReader(fr);
	}
	return null;
    }
    
    generator FileReaderr genFileReaderr(boolean[] localBools, Object[] localObjs) {
	if (??) { return localObjs[3]; }
	if (??) {
	    String fname = genString(localBools, localObjs);
	    return new FileReaderr(fname);
	}
	return null;
    }
    
    generator boolean guard(boolean[] localBools, Object[] localObjs) {
	boolean cond = false;
	if (??) { cond = localBools[0]; }
	if (??) {
	    int i = {| 0,1,2,3,4,5 |};
	    cond = localObjs[i] == null;
	}
	return {| cond, !cond |};
    }

    generator void voidFuncs(boolean[] localBools, Object[] localObjs) {
	if (??) {
	    // ArrayList<String> values = genArrayList(localBools, localObjs);
	    ArrayList<String> values = localObjs[2];
	    values.sort(null);
	}
	// if (??) {
	//     String vbar = genString(localBools, localObjs);
	//     ArrayList<String> values2 = genArrayList(localBools, localObjs);
	//     String fname2 = genString(localBools, localObjs);
	//     values2.add(vbar.concat(fname2));
	// }
	// if (??) {
	//     FileReaderr fr2 = genFileReaderr(localBools, localObjs);
	//     fr2.close();
	// }
    }
    
    generator void stmts(boolean[] localBools, Object[] localObjs) {
	// if (??) { localBools[0] = guard(localBools, localObjs); }
	// if (??) { localObjs[0] = genString(localBools, localObjs); }
	// if (??) { localObjs[1] = genString(localBools, localObjs); }
	// if (??) { localObjs[2] = genArrayList(localBools, localObjs); }
	// if (??) { localObjs[3] = genFileReaderr(localBools, localObjs); }
	// if (??) { localObjs[4] = genBufferedReader(localBools, localObjs); }
	// if (??) { localObjs[5] = genString(localBools, localObjs); }
	if (??) { voidFuncs(localBools, localObjs); }
	// if (??) { stmts(localBools, localObjs); }
    }
    
        /**
         * Function is creating diff.txt file
         * @param  arg filename name of the file to be loaded
         * @param  arg true for list of values
         */
        public ArrayList<String> ReadToArray(String filename,boolean isAList ) throws IOException{    
    
	    boolean[] localBools = new boolean[1];
	    localBools[0] = isAList;
	    Object[] localObjs = new Object[6];
	    localObjs[0] = filename;

	    localObjs[1] = null;
	    localObjs[2] = new ArrayList<String>();
	    String fname = (String) localObjs[0];
	    localObjs[3] = new FileReaderr(fname);
	    FileReaderr fr = (FileReaderr) localObjs[3];
	    localObjs[4] = new BufferedReader(fr);

	    // stmts(localBools, localObjs);	    
	    // stmts(localBools, localObjs);
	    // stmts(localBools, localObjs);	    

	    if (??) {
	    	// ArrayList<String> values = genArrayList(localBools, localObjs);
	    	ArrayList<String> values = localObjs[2];
	    	values.sort(null);
	    }
	    
	    // ArrayList<String> values = (ArrayList<String>) localObjs[2];
	    // values.sort(null);

	    BufferedReader br = (BufferedReader) localObjs[4];
	    localObjs[1] = br.readLine();	   
	    
	    while(localObjs[1] != null) {		
		if (localObjs[1] != null && !localBools[0] == true){
		    // stmts(localBools,localObjs);
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
	} 
                               
        /**
         * Function is removing duplicated lines from ArrayList<String>
         * @param  toBeSorted - array to be sorted
         * @return ArrayList<String> without duplicated lines
         */
        public ArrayList<String> RemoveDuplicates(ArrayList<String> toBeSorted){
            int j=1;

	    Object[] localObjs = new Object[6];
	    localObjs[2] = toBeSorted;
	    boolean[] localBools = new boolean[1];

	    // stmts(localBools, localObjs);
	    
	    toBeSorted.sort(null);
		
	    while(j+1<toBeSorted.size()){
		String get_j = toBeSorted.get(j);
		String sstr = get_j.substring(0, get_j.indexOf("|"));
		String get_j1 = toBeSorted.get(j+1);
		String sstr1 = get_j1.substring(0, get_j1.indexOf("|"));
		if (sstr.equals(sstr1)) {
            //     if( toBeSorted.get(j).substring(0,toBeSorted.get(j).indexOf("|")).equals(toBeSorted.get(j+1).substring(0,toBeSorted.get(j+1).indexOf("|")) )){
		    if (??) {
                	toBeSorted.remove(j+1);
                        toBeSorted.remove(j);
		    }
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

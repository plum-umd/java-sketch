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

        /**
         * Function is creating diff.txt file
         * @param  arg filename name of the file to be loaded
         * @param  arg true for list of values
         */
        public ArrayList<String> ReadToArray(String filename,boolean isAList ) throws IOException{    
    
                FileReader fr = null;
                String value = "";
                
                ArrayList<String> values = new ArrayList<String>();
                Collections.sort(values);
                    try {
                            fr = new FileReader(filename);
                        } catch (FileNotFoundException e1) {
                                System.out.println("Error opening the file (file not found)");
                                    System.exit(1);
                            }
                        BufferedReader bfr = new BufferedReader(fr);
                            try {    
                                while((value = bfr.readLine()) != null){  
                                     if (value!=null && !isAList==true){
                                        values.add(value+"|"+filename);  
                                    }               
                                }
                                } catch (IOException e) {
                                        System.out.println("Error reading the file");
                                            System.exit(2);
                                    }

                                try {
                                        fr.close();
                                    } catch (IOException e11) {
                                        System.out.println("Error closing the file");
                                        System.exit(3);
                                        }
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
                if( toBeSorted.get(j).substring(0,toBeSorted.get(j).indexOf("|")).equals(toBeSorted.get(j+1).substring(0,toBeSorted.get(j+1).indexOf("|")) )){
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
    
            FileWriter fileWriter = new FileWriter(filename);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter); 

            try{
                for(int k=0;k<= rows.size()-1;k++){     
                            bufferedWriter.write(rows.get(k));
                            bufferedWriter.newLine();
                }
            }finally{
                bufferedWriter.close();
                System.out.println(filename+" was created");
            }
        }

        /**
         * Function is clearing chosen file
         * @param  name of the file to be cleared
         */
        public void ClearFile(String toBeCleared) throws IOException{
            FileWriter fileWriter = new FileWriter(toBeCleared);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter); 
            
            bufferedWriter.close();
            

        }   
        
        
}

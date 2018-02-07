package easycsv;

import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

import static easycsv.CodeAssertion.verifyThat;

/**
 * Created by Dan Geabunea on 3/24/15.
 */
public class CsvDocument {
    private ArrayList<CsvRow> csvRows;

    public CsvDocument(ArrayList<CsvRow> csvRows){
        // verifyThat(csvRows != null, EasyCsvErrorMessages.nullValue("csvRows"));
        // verifyThat(csvRows.size() > 0, EasyCsvErrorMessages.emptyList("csvRows"));

        this.csvRows = csvRows;
    }

    public ArrayList<CsvRow> getCsvRows() {
        return csvRows;
    }

    /**
     * Boolean flag for determining if a CSV document is empty (does not have any rows/content)
     */
    public boolean isEmpty(){
        return this.csvRows.size() == 0;
    }

    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        // for(CsvRow row : this.csvRows){
	int size = csvRows.size();
        for(int i = 0; i < size; i++) {
	    CsvRow row = csvRows.get(i);
            sb.append(row.toString());
        }
        return sb.toString();
    }

    /**
     * Reads the content of a csv file and transforms it into a CsvDocument object
     * @param filePath The absolute file path to the csv file
     * @throws IOException
     */
    public static CsvDocument read(String filePath) throws IOException {
        CsvConfiguration defaultConfiguration = new CsvConfiguration();
        return CsvDocument.read(filePath, defaultConfiguration);
    }

    generator public static CsvDocument genRead(BufferedReader bufferedReader, CsvConfiguration csvConfiguration, ArrayList<CsvRow> parsedCsvRows) {
	String csvLine = null;
	CsvRow row = null;
	CsvDocument parsedDocument = null;
	if (??) {
	    if (csvConfiguration.skipHeader()) {
		bufferedReader.readLine();
	    }
	}
	if (??) {
	    csvLine = bufferedReader.readLine();	    
	}
	if (??) {
	    parsedCsvRows.add(row);
	}
	if (??) {
	    row = parseCsvRow(csvConfiguration, csvLine);
	}
	if (??) {
	    genRead(bufferedReader, csvConfiguration, parsedCsvRows);
	}
	if (??) {
	    parsedDocument = new CsvDocument(parsedCsvRows);	
	}

	return parsedDocument;
    }
    
    /**
     * Reads the content of a csv file and transforms it into a CsvDocument object
     * @param filePath The absolute file path to the csv file
     * @param csvConfiguration a configuration object that dictates how the csv parsing will take place
     * @throws IOException
     */
    public static CsvDocument read(String filePath, CsvConfiguration csvConfiguration) throws IOException {
        // verifyThat(filePath != null, EasyCsvErrorMessages.nullValue("filePath"));
        // verifyThat(csvConfiguration != null, EasyCsvErrorMessages.nullValue("csvConfiguration"));

	BufferedReader bufferedReader = new BufferedReader(new FileReaderr(filePath));

	ArrayList<CsvRow> parsedCsvRows = new ArrayList<>();	
        // try (BufferedReader bufferedReader = new BufferedReader(new FileReader(filePath))) {
	//skip header
	// if (csvConfiguration.skipHeader()) {
	//     bufferedReader.readLine();
	// }

	genRead(bufferedReader, csvConfiguration, parsedCsvRows);
	
	//parse rows
	String csvLine = bufferedReader.readLine();
	while (csvLine != null) {
	    genRead(bufferedReader, csvConfiguration, parsedCsvRows);
	    // CsvRow row = parseCsvRow(csvConfiguration, csvLine);
	    // parsedCsvRows.add(row);
	    // csvLine = bufferedReader.readLine();	    
	}

	//build document
	// CsvDocument parsedDocument = new CsvDocument(parsedCsvRows);

	// return parsedDocument;
	return genRead(bufferedReader, csvConfiguration, parsedCsvRows);
        // }
    }

    // /**
    //  * Reads the content of a csv file and transforms it into a CsvDocument object
    //  * @param filePath The absolute file path to the csv file
    //  * @param csvConfiguration a configuration object that dictates how the csv parsing will take place
    //  * @throws IOException
    //  */
    // public static CsvDocument read(String filePath, CsvConfiguration csvConfiguration) throws IOException {
    //     // verifyThat(filePath != null, EasyCsvErrorMessages.nullValue("filePath"));
    //     // verifyThat(csvConfiguration != null, EasyCsvErrorMessages.nullValue("csvConfiguration"));

    // 	BufferedReader bufferedReader = new BufferedReader(new FileReaderr(filePath));
	
    //     // try (BufferedReader bufferedReader = new BufferedReader(new FileReader(filePath))) {
    // 	//skip header
    // 	if (csvConfiguration.skipHeader()) {
    // 	    bufferedReader.readLine();
    // 	}

    // 	//parse rows
    // 	String csvLine = bufferedReader.readLine();
    // 	ArrayList<CsvRow> parsedCsvRows = new ArrayList<>();
    // 	while (csvLine != null) {
    // 	    CsvRow row = parseCsvRow(csvConfiguration, csvLine);
    // 	    parsedCsvRows.add(row);
    // 	    csvLine = bufferedReader.readLine();	    
    // 	}

    // 	//build document
    // 	CsvDocument parsedDocument = new CsvDocument(parsedCsvRows);

    // 	return parsedDocument;
    //     // }
    // }

    /**
     * Writes the content of the csv document to the given path on disk. If the file does not exist, it will
     * be created
     * @param document the csv document to be written to a file
     * @param savePath the absolute file path where the csv document will be written
     */
    public static boolean tryWriteToFile(CsvDocument document, String savePath){
        // try (PrintStream out = new PrintStream(new FileOutputStream(savePath))) {
        PrintStream out = new PrintStream(new FileOutputStream(savePath));
	out.print(document.toString());
	out.close();
	return true;
        // } catch (FileNotFoundException e) {
        //     e.printStackTrace();
        //     return false;
        // }
    }

    private static CsvRow parseCsvRow(CsvConfiguration csvConfiguration, String csvLine) {
        final String COMA_SEPARATOR = ",";
        String[] columns = csvLine.split(COMA_SEPARATOR);

        ArrayList<CsvColumn> csvColumns = new ArrayList<>();
        if(csvConfiguration.parseAllColumns()){
            for(int i=0; i<columns.length;i++){
                csvColumns.add(new CsvColumn(columns[i]));
            }
        }
        else{
           // for(int columnIndex : csvConfiguration.getColumnIndexesToParse()){
	   ArrayList<Integer> colInds = csvConfiguration.getColumnIndexesToParse();
	   int size = colInds.size();
	   for (int i = 0; i < size; i++) {
	       Integer columnIndexInt = colInds.get(i);
	       int columnIndex = columnIndexInt.intValue();
	       csvColumns.add(new CsvColumn(columns[columnIndex]));
           }
        }

        return new CsvRow(csvColumns);
    }
}

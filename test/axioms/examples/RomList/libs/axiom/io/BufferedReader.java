@axiomClass
public class BufferedReader {
    @adt
    @constructor
    BufferedReader BufferedReader(File type);

    @adt
    String readLine();

    @adt
    String readLineHelp(int i);
    
    axiom Object readLine(Object BufferedReader(File f)) {
    	// String[] parts = f.data.split("\n");
    	// return parts[0];	
	// return f.data.splitGetEl("\n", 0);
	return f.get(0);
    }

    axiom Object readLine(Object readLine!(BufferedReader b)) {
    	return readLineHelp(b, 1);
    }

    axiom Object readLineHelp(Object readLine!(BufferedReader b), int i) {
    	return readLineHelp(b, i+1);
    }

    axiom Object readLineHelp(Object BufferedReader(File f), int i) {
    	// String[] parts = f.data.split("\n");
    	// return i < parts.length ? parts[i] : null;
	// return parts[i];
	// return f.data.splitGetEl("\n", i);	
	return f.get(i);
    }

}

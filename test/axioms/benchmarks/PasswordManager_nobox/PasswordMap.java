import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map.Entry;

// import org.apache.commons.codec.DecoderException;
// import org.apache.commons.codec.binary.Base64;

public class PasswordMap {

        HashMap<String, String> passMap;
	public String masterHash;

	    // throws IOException, DecoderException,
	    // 	ClassNotFoundException
    
	public PasswordMap()     {
		// loadMapFromFile();
		// loadMasterPassword();
	    passMap = new HashMap<String, String>();
	    // masterHash = "Secret Password";
	    Cryptographer c = new Cryptographer();
	    masterHash = c.hash("1234");
	}

	// private void loadMasterPassword() throws IOException,
	// 		ClassNotFoundException {
	// 	FileInputStream fis = new FileInputStream("MasterPassHash");
	// 	ObjectInputStream ois = new ObjectInputStream(fis);
	// 	masterHash = (String) ois.readObject();
	// 	ois.close();
	// 	fis.close();
	// }

	public void add(String tag, String passEncryption) {
		passMap.put(tag, passEncryption);
	}

	public void remove(String tag) {
		if (passMap.containsKey(tag))
			passMap.remove(tag);
	}

	public String get(String domainHash) {
		return passMap.get(domainHash);
	}

	// public void loadMapFromFile() throws IOException, DecoderException {

	// 	try {
	// 		FileInputStream fis = new FileInputStream("passMap.ser");
	// 		ObjectInputStream ois = new ObjectInputStream(fis);
	// 		passMap = (HashMap<String, String>) ois.readObject();
	// 		ois.close();
	// 		fis.close();
	// 	} catch (IOException ioe) {
	// 		ioe.printStackTrace();
	// 		return;
	// 	} catch (ClassNotFoundException c) {
	// 		System.out.println("Class not found");
	// 		c.printStackTrace();
	// 		return;
	// 	}

	// }

	// public void saveMapToFile() throws FileNotFoundException {
	// 	PrintWriter printWrite = new PrintWriter(new File("passMap.ser"));

	// 	try {
	// 		FileOutputStream fos = new FileOutputStream("passMap.ser");
	// 		ObjectOutputStream oos = new ObjectOutputStream(fos);
	// 		oos.writeObject(passMap);
	// 		oos.close();
	// 		fos.close();
	// 	} catch (IOException ioe) {
	// 		ioe.printStackTrace();
	// 	}

	// 	try {
	// 		FileOutputStream fos = new FileOutputStream("MasterPassHash");
	// 		ObjectOutputStream oos = new ObjectOutputStream(fos);
	// 		oos.writeObject(new String("55124a287e8ddc58a97eb3eea634a4d3185428d552de1a2b5bd49511355ababa"));
	// 		oos.close();
	// 		fos.close();
	// 	} catch (IOException ioe) {
	// 		ioe.printStackTrace();
	// 	}

	// }

}

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.spec.InvalidParameterSpecException;
import java.sql.Savepoint;

import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.security.sasl.AuthenticationException;

// import org.apache.commons.codec.DecoderException;

public class PasswordManager {

	/**
	 * @param args
	 * @throws AuthenticationException
	 */

	private static PasswordManager passManager;
	private Cryptographer cryptographer;
	private PasswordMap passMap;

	    // throws NoSuchAlgorithmException, NoSuchPaddingException,
	    // 	NoSuchProviderException, InvalidKeyException,
	    // 	InvalidParameterSpecException, InvalidAlgorithmParameterException,
	    // 	IOException, DecoderException, ClassNotFoundException 

    
        public static PasswordManager getPassManager(String masterPassword) {
		if (passManager != null)
			return passManager;
		passManager = new PasswordManager(masterPassword);
		return passManager;
	}

	// private PasswordManager() throws AuthenticationException,
	// 		InvalidKeyException, NoSuchAlgorithmException,
	// 		NoSuchPaddingException, NoSuchProviderException,
	// 		InvalidParameterSpecException, InvalidAlgorithmParameterException {
	// 	throw new AuthenticationException("Master Password is required");
	// }


     // throws NoSuchAlgorithmException, NoSuchPaddingException,
     // 	    NoSuchProviderException, InvalidKeyException,
     // 	    InvalidParameterSpecException, InvalidAlgorithmParameterException,
     // 	    IOException, DecoderException, ClassNotFoundException 
    
	// authentication is required only on creation
	public PasswordManager(String masterPassword) {
		cryptographer = new Cryptographer();
		passMap = new PasswordMap();
		// if (!checkMasterPassword(masterPassword))
		// 	throw new AuthenticationException("worng Master Password");
	}

	private boolean checkMasterPassword(String masterPassword) {
		// TODO Auto-generated method stub
		String passHash = cryptographer.hash(masterPassword);
		boolean beq =  passHash.equals(passMap.masterHash);
		boolean b = {| beq, passHash == passMap.masterHash |};
		// if (passHash.equals(passMap.masterHash))
		if (b)
			return true;
		return false;
	}


        // throws InvalidKeyException, IllegalBlockSizeException,
	//     BadPaddingException, InvalidAlgorithmParameterException 
    
	public void addPassword(String domain, String passWord){
		String PassEncryption = cryptographer.encrypt(passWord);
		assert !passWord.equals(PassEncryption);
		String domainHash = cryptographer.hash(domain);
		passMap.add(domainHash, PassEncryption);

	}


	// throws InvalidKeyException, IllegalBlockSizeException,
	//     BadPaddingException, InvalidAlgorithmParameterException 
    
	public void modifyPassword(String domain, String passWord) {
		String PassEncryption = cryptographer.encrypt(passWord);
		assert !passWord.equals(PassEncryption);
		String domainHash = cryptographer.hash(domain);
		passMap.add(domainHash, PassEncryption);
	}

	public void deletePassword(String domain) {
		String domainHash = cryptographer.hash(domain);
		passMap.remove(domainHash);
	}

        // throws InvalidKeyException,
	//     NoSuchAlgorithmException, NoSuchPaddingException,
	//     UnsupportedEncodingException, IllegalBlockSizeException,NullPointerException
	//     ,BadPaddingException, DecoderException, InvalidAlgorithmParameterException
    
	public String getPass(String domain) {
		String domainHash = cryptographer.hash(domain);
		String PassEncryption = passMap.get(domainHash);
		return cryptographer.decrypt(PassEncryption);
	}

        // throws IOException, DecoderException
    
        public void close() {
		// passMap.saveMapToFile();
		// System.out.println("before saving");
		// System.out.println(passMap.passMap.toString());

		// passMap.loadMapFromFile();
		// System.out.println("after saving");
		// System.out.println(passMap.passMap.toString());
	}

        public void changeMaster(String newMaster) throws FileNotFoundException{
		String passHash = cryptographer.hash(newMaster);
		passMap.masterHash = passHash;
		// passMap.saveMapToFile();
	}

    // public static void main(/*String[] args*/) throws InvalidKeyException,
    // 			IllegalBlockSizeException, BadPaddingException,
    // 			NoSuchAlgorithmException, NoSuchPaddingException,
    // 			NoSuchProviderException, IOException,
    // 			InvalidParameterSpecException, InvalidAlgorithmParameterException,
    // 			DecoderException, ClassNotFoundException {
    // 		PasswordManager pasman = new PasswordManager("1234");
    // 		System.out.println("Adding  pair: yahoo, pass:12345");
    // 		System.out.println("adding pair: google, pass:5441944");
    // 		pasman.addPassword("yahoo", "12345");
    // 		pasman.addPassword("google", "5441944");
    // 		pasman.deletePassword("google");
    // 		//pasman.modifyPassword("google", "5115");		
    // 		// try{
			
    // 		// 	String s = pasman.getPass("google");
    // 		// 	System.out.println("Password for google.com is : "+s);
    // 		// }catch (NullPointerException e) {
    // 		// 	System.err.println("Password not found");
    // 		// }

    // 	}

}

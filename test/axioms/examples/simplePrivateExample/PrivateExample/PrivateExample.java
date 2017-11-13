/*
 Encrypt and decrypt using the DES private key algorithm
*/
// import java.security.*;
// import javax.crypto.*;

public class PrivateExample {

    harness void test_privateExample() {
	String plainText = "Secret Message!";

	byte[] newPlainText = privateExample(plainText);

	String plainText2 = new String(newPlainText);
	
	assert plainText.equals(plainText2);
    }
    
    public static byte[] privateExample(String plainTextString) {
        // // Check args and get plaintext
        // if (args.length !=1) {
        //     // System.err.println("Usage: java PrivateExample text");
        //     // System.exit(1);
    	//     assert false;
        // }

	byte[] plainText = plainTextString.getBytes();
	
        // Get a DES private key
        KeyGenerator keyGen = KeyGenerator.getInstance("DES");
        
        // If you do not initialize the KeyGenerator, each provider supply a default initialization.
        keyGen.init(56);
        Key key = keyGen.generateKey();

        // Creates the DES Cipher object (specifying the algorithm, mode, and padding).
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");

        // Initializes the Cipher object.
        // cipher.init(Cipher.ENCRYPT_MODE, key);
        cipher.init(1, key);
        // Encrypt the plaintext using the public key
        byte[] cipherText = cipher.doFinal(plainText);

        // Initializes the Cipher object.
        // cipher.init(Cipher.DECRYPT_MODE, key);
        cipher.init(2, key);
        // Decrypt the ciphertext using the same key
        byte[] newPlainText = cipher.doFinal(cipherText);

    	return newPlainText;
    }
}

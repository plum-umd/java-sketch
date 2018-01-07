import java.io.UnsupportedEncodingException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import java.security.Security;
import java.security.spec.InvalidParameterSpecException;
import java.util.Formatter;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.Mac;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

// import org.apache.commons.codec.DecoderException;
// import org.apache.commons.codec.binary.Hex;

/**
 * functionality of encription and decreption
 * 
 * @author azmy
 * 
 */
public class Cryptographer {

	public SecretKey GCMSecretKey; // AES/GCM key
	public SecretKeySpec Hash_secret_key; // HMAC secret key
	private Mac sha256_HMAC;
	private Cipher myCypherOut;
	byte[] randomIv;
	IvParameterSpec ivParameterSpec;
	// final int MAX_LENGTH_PASSWORD = 16;    
	private int MAX_LENGTH_PASSWORD;
    
        public Cryptographer() // throws NoSuchAlgorithmException,
			// NoSuchPaddingException, NoSuchProviderException,
			// InvalidKeyException, InvalidAlgorithmParameterException
        {
		// Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());
		SecureRandom random = new SecureRandom();

		byte[] randomKey = new byte[16];
		random.nextBytes(randomKey);
		
		// GCMSecretKey = new SecretKeySpec(randomKey, "AES");
		GCMSecretKey = new SecretKeySpec();
		
		randomIv = new byte[16];
		random.nextBytes(randomIv);
		ivParameterSpec = new IvParameterSpec(randomIv);
				
		// myCypherOut = Cipher.getInstance("AES/GCM/NoPadding", "BC");
		myCypherOut = new Cipher();
		// // myCypherOut.init(Cipher.DECRYPT_MODE, GCMSecretKey,ivParameterSpec);
		myCypherOut.init(2, GCMSecretKey,ivParameterSpec);
		
		// init HMAC
		String secret = "secret";
		// sha256_HMAC = Mac.getInstance("HmacSHA256");
		sha256_HMAC = new Mac();
		// Hash_secret_key = new SecretKeySpec(secret.getBytes(), "HmacSHA256");
		Hash_secret_key = new SecretKeySpec();
		sha256_HMAC.init(Hash_secret_key);

		MAX_LENGTH_PASSWORD = 16;
	}

    	public String hash(String plainTxt) {
    		// return toHexString(sha256_HMAC.doFinal(plainTxt.getBytes()));
    	    // return new String(sha256_HMAC.doFinal(plainTxt));
    	    return sha256_HMAC.doFinal(plainTxt);
    	}

    generator byte[] genCipherText(String plainText) {
	byte[] cipherText;

	if (??) myCypherOut.init(??, GCMSecretKey, ivParameterSpec);
	if (??) cipherText = myCypherOut.doFinal(plainText.getBytes());
	if (??) cipherText = genCipherText(plainText);
	
	return cipherText;
    }
    
    // Throws InvalidKeyException,
    // IllegalBlockSizeException, BadPaddingException,
    // InvalidAlgorithmParameterException
    	public String encrypt(String plainText)         {
    		// if(plainText.length()<MAX_LENGTH_PASSWORD){	
    		// 	int paddedPart  = plainText.length(); 
    		// 	for (int i = paddedPart  ; i < MAX_LENGTH_PASSWORD; i++) {
    		// 		// plainText =plainText +  paddedPart;
    		// 	    plainText = plainText.concat("0");
    		// 	}
    		// }
    		// myCypherOut.init(Cipher.ENCRYPT_MODE, GCMSecretKey,ivParameterSpec);
    		myCypherOut.init(1, GCMSecretKey,ivParameterSpec);
    		byte[] cipherText = myCypherOut.doFinal(plainText.getBytes());
    		// return toHexString(cipherText);
    		return new String(cipherText);
    	}

     // throws InvalidKeyException,
     // 	    NoSuchAlgorithmException, NoSuchPaddingException,
     // 	    UnsupportedEncodingException, IllegalBlockSizeException,
     // 	    BadPaddingException, InvalidAlgorithmParameterException
    
    	public String decrypt(String cipherText)    {

    		// myCypherOut.init(Cipher.DECRYPT_MODE, GCMSecretKey,ivParameterSpec);
    		myCypherOut.init(2, GCMSecretKey,ivParameterSpec);
    		// String decryptText = new String(
    		// 		myCypherOut.doFinal(hexStringToByteArray(cipherText)));
    		byte[] plainText = myCypherOut.doFinal(cipherText.getBytes());
    		String decryptText = new String(plainText);  			

    		// if(decryptText.charAt(decryptText.length()-1)<='9'&&decryptText.charAt(decryptText.length()-1)>='0')
    		// {
    		// 	int beforePad = Integer.parseInt(""+decryptText.charAt(decryptText.length()-1));
    		// 	decryptText = decryptText.substring(0,beforePad);
    		// }
		
    		return decryptText;
    	}

    //    // harness public static void main()//String[] args) // throws NoSuchAlgorithmException,
    //    // 			// NoSuchPaddingException, NoSuchProviderException,
    //    // 			// InvalidKeyException, UnsupportedEncodingException,
    //    // 			// IllegalBlockSizeException, BadPaddingException, DecoderException, InvalidAlgorithmParameterException
    //    // {
    //    // 		Cryptographer gcm = new Cryptographer();
    //    // 		//System.out.println(gcm.decrypt((gcm.encrypt("hi man"))));
    //    // 		// System.out.println(gcm.hash("1234"));

    //    // 	}

    // 	// public static byte[] hexStringToByteArray(String s) {
    // 	// 	int len = s.length();
    // 	// 	byte[] data = new byte[len / 2];
    // 	// 	for (int i = 0; i < len; i += 2) {
    // 	// 		data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4) + Character
    // 	// 				.digit(s.charAt(i + 1), 16));
    // 	// 	}
    // 	// 	return data;
    // 	// }

    // 	// public static String toHexString(byte[] bytes) {
    // 	// 	Formatter formatter = new Formatter();
    // 	// 	for (byte b : bytes) {
    // 	// 		formatter.format("%02x", b);
    // 	// 	}

    // 	// 	return formatter.toString();
    // 	// }
}

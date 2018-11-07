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
    
    generator public Object genCipherText(String plainText) {
	@isBoxed
	byte[] cipherText = null;
	if (??) { myCypherOut.init(??, GCMSecretKey, ivParameterSpec); }
	if (??) {
	    @box
	    byte[] plainText_bytes = plainText.getBytes();
	    
	    cipherText = myCypherOut.doFinal(plainText_bytes);
	}
	if (??) { cipherText = genCipherText(plainText); }
	return cipherText;
    }

    generator public byte[] genCipherText2(String plainText) {
	byte[] cipherText;
	if (??) { myCypherOut.init(??, GCMSecretKey, ivParameterSpec); }
	if (??) {
	    @unbox
	    byte[] answer = myCypherOut.doFinal(plainText);
	    cipherText = answer;
	}
	if (??) { cipherText = genCipherText2(plainText); }
	return cipherText;
    }

    generator SecretKeySpec genSecretKeySpec(int[] localInts, Object[] localObjs) {
	if (??) { return localObjs[2]; }
	if (??) {
	    return new SecretKeySpec();
	}
	return null;
    }

    generator IvParameterSpec genIvParameterSpec(int[] localInts, Object[] localObjs) {
	if (??) { return localObjs[3]; }
	if (??) {
	    byte[] bs = genBytes(localInts, localObjs);
	    return new IvParameterSpec(bs);
	}
	return null;
    }
    
    generator byte[] genBytes(int[] localInts, Object[] localObjs) {
	if (??) {
	    Bytes bytes = (Bytes) localObjs[1];
	    return bytes.toArray();
	}
	if (??) {
	    String plainText = genString(localInts, localObjs);
	    Cipher c = genCipher(localInts, localObjs);
	    @unbox
	    byte[] answer = c.doFinal(plainText);
	    return answer;		
	}
	return new byte[1];
    }

    generator Cipher genCipher(int[] localInts, Object[] localObjs) {
	if (??) { return (Cipher) localObjs[0]; }
	return null;
    }
    
    generator String genString(int[] localInts, Object[] localObjs) {
	if (??) { return (String) localObjs[2]; }
	if (??) { return (String) localObjs[4]; }
	if (??) {
	    String plainText = genString(localInts, localObjs);
	    @box
	    byte[] plainText_bytes = plainText.getBytes();
	    Cipher c = genCipher(localInts, localObjs);
	    @isBoxed
	    byte[] cipherText = c.doFinal(plainText_bytes);
	    return cipherText;
	}
	if (??) {
	    byte[] bs = genBytes(localInts, localObjs);
	    return new String(bs);
	}
	return null;
    }
    
    generator int genInt(int[] localInts, Object[] localObjs) {
	int i1 = localInts[0];
	return {| i1, ?? |};
    }
    
    generator void voidFuncs(int[] localInts, Object[] localObjs) {
	if (??) {
	    Cipher c = genCipher(localInts, localObjs);
	    int i = genInt(localInts, localObjs);
	    SecretKeySpec k = genSecretKeySpec(localInts, localObjs);
	    IvParameterSpec iv = genIvParameterSpec(localInts, localObjs);
	    c.init(i, k, iv);
	}
    }
    
    generator void stmts(int[] localInts, Object[] localObjs) {
	if (??) { localObjs[??] = genString(localInts, localObjs); }
	if (??) { voidFuncs(localInts, localObjs); }
	if (??) { stmts(localInts, localObjs); }
    }
    
    public String encrypt(String plainText) {
	// @isBoxed
	// byte[] cipherText = genCipherText(plainText);
	// // return new String(cipherText);
	// // return myCypherOut.toString();
	// return cipherText;

	int[] localInts = new int[1];
	localInts[0] = MAX_LENGTH_PASSWORD;
	Object[] localObjs = new Object[5];
	localObjs[0] = myCypherOut;
	localObjs[2] = GCMSecretKey;
	localObjs[3] = ivParameterSpec;
	localObjs[4] = plainText;
	stmts(localInts, localObjs);
	myCypherOut = localObjs[0];
	GCMSecretKey = localObjs[2];
	ivParameterSpec = localObjs[3];
	return genString(localInts, localObjs);
    }
    
    // // throws InvalidKeyException,
    // // IllegalBlockSizeException, BadPaddingException,
    // // InvalidAlgorithmParameterException
    // 	public String encrypt(String plainText)         {
    // 		// if(plainText.length()<MAX_LENGTH_PASSWORD){	
    // 		// 	int paddedPart  = plainText.length(); 
    // 		// 	for (int i = paddedPart  ; i < MAX_LENGTH_PASSWORD; i++) {
    // 		// 		// plainText =plainText +  paddedPart;
    // 		// 	    plainText = plainText.concat("0");
    // 		// 	}
    // 		// }
    // 		// myCypherOut.init(Cipher.ENCRYPT_MODE, GCMSecretKey,ivParameterSpec);
    // 	        // should be 1
    // 		myCypherOut.init(??, GCMSecretKey,ivParameterSpec);
    // 		byte[] cipherText = myCypherOut.doFinal(plainText.getBytes());
    // 		// return toHexString(cipherText);
    // 		return new String(cipherText);
    // 	}

    public String decrypt(String plainText) {
	int[] localInts = new int[1];
	localInts[0] = MAX_LENGTH_PASSWORD;
	Object[] localObjs = new Object[5];
	localObjs[0] = myCypherOut;
	localObjs[2] = GCMSecretKey;
	localObjs[3] = ivParameterSpec;
	localObjs[4] = plainText;
	stmts(localInts, localObjs);
	myCypherOut = localObjs[0];
	GCMSecretKey = localObjs[2];
	ivParameterSpec = localObjs[3];
	return genString(localInts, localObjs);
	// byte[] cipherText = genCipherText2(plainText);
	// return new String(cipherText);
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

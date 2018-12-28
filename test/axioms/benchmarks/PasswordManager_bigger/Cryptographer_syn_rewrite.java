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
    
        public Cryptographer() {
	    Object[] localObjs = new Object[2];

	    stmts(localObjs);
	    
	    // SecureRandom random = new SecureRandom();

	    // byte[] randomKey = new byte[16];
	    // random.nextBytes(randomKey);

	    // // GCMSecretKey = new SecretKeySpec(randomKey, "AES");
	    // GCMSecretKey = new SecretKeySpec();

	    // randomIv = new byte[16];
	    // random.nextBytes(randomIv);
	    // ivParameterSpec = new IvParameterSpec(randomIv);

	    // // myCypherOut = Cipher.getInstance("AES/GCM/NoPadding", "BC");
	    // myCypherOut = new Cipher();
	    // // // myCypherOut.init(Cipher.DECRYPT_MODE, GCMSecretKey,ivParameterSpec);
	    // myCypherOut.init(2, GCMSecretKey,ivParameterSpec);

	    // String secret = "secret";
	    // // sha256_HMAC = Mac.getInstance("HmacSHA256");
	    // sha256_HMAC = new Mac();
	    // // Hash_secret_key = new SecretKeySpec(secret.getBytes(), "HmacSHA256");
	    // Hash_secret_key = new SecretKeySpec();
	    // sha256_HMAC.init(Hash_secret_key);
	    // MAX_LENGTH_PASSWORD = 16;	    
	}

    	public String hash(String plainTxt) {
    		// return toHexString(sha256_HMAC.doFinal(plainTxt.getBytes()));
    	    // return new String(sha256_HMAC.doFinal(plainTxt));
    	    return sha256_HMAC.doFinal(plainTxt);
    	}
    
    generator Mac genMac(Object[] localObjs) {
	if (??) { return sha256_HMAC; }
	if (??) { return new Mac(); }
	return null;
    }
    
    generator SecretKeySpec genSecretKeySpec(Object[] localObjs) {
	if (??) { return GCMSecretKey; }
	if (??) {
	    byte[] bs2 = genBytes(localObjs);
	    Bytes bs = new Bytes(bs2);
	    return new SecretKeySpec(bs);
	    // return new SecretKeySpec();
	}
	return null;
    }

    generator IvParameterSpec genIvParameterSpec(Object[] localObjs) {
	if (??) { return ivParameterSpec; }
	if (??) {
	    byte[] bs = genBytes(localObjs);
	    return new IvParameterSpec(bs);
	}
	return null;
    }
    
    generator byte[] genBytes(Object[] localObjs) {
	if (??) {
	    Bytes bytes = (Bytes) localObjs[1];
	    return bytes.toArray();
	}
	if (??) {
	    String plainText = genString(localObjs);
	    Cipher c = genCipher(localObjs);
	    @unbox
	    byte[] answer = c.doFinal(plainText);
	    return answer;		
	} if (??) {
	    SecureRandom random = new SecureRandom();
	    byte[] randomKey = new byte[16];
	    random.nextBytes(randomKey);
	    return randomKey;
	}
	return new byte[16];
    }

    generator Cipher genCipher(Object[] localObjs) {
	if (??) { return myCypherOut; }
	if (??) { return new Cipher(); }
	return null;
    }
    
    generator String genString(Object[] localObjs) {
	if (??) { return (String) localObjs[0]; }
	if (??) {
	    String plainText = genString(localObjs);
	    @box
	    byte[] plainText_bytes = plainText.getBytes();
	    Cipher c = genCipher(localObjs);
	    @isBoxed
	    byte[] cipherText = c.doFinal(plainText_bytes);
	    return cipherText;
	}
	if (??) {
	    byte[] bs = genBytes(localObjs);
	    return new String(bs);
	}
	return null;
    }
    
    generator int genInt(Object[] localObjs) {
	return {| MAX_LENGTH_PASSWORD, ?? |};
    }
    
    generator void voidFuncs(Object[] localObjs) {
	if (??) {
	    Cipher c = genCipher(localObjs);
	    int i = genInt(localObjs);
	    SecretKeySpec k = genSecretKeySpec(localObjs);
	    IvParameterSpec iv = genIvParameterSpec(localObjs);
	    c.init(i, k, iv);
	}
	if (??) {
	    Mac m = genMac(localObjs);
	    SecretKeySpec s = genSecretKeySpec(localObjs);
	    m.init(s);
	}
    }
    
    generator void stmts(Object[] localObjs) {
	if (??) { voidFuncs(localObjs); }
	if (??) { localObjs[0] = genString(localObjs); }
	if (??) {
	    byte[] bs = genBytes(localObjs);
	    localObjs[1] = new Bytes(bs);
	}	
	if (??) { myCypherOut = genCipher(localObjs); }
	if (??) { GCMSecretKey = genSecretKeySpec(localObjs); }
	if (??) { ivParameterSpec = genIvParameterSpec(localObjs); }
	if (??) { sha256_HMAC = genMac(localObjs); }
	if (??) { MAX_LENGTH_PASSWORD = genInt(localObjs); }
	if (??) { stmts(localObjs); }
    }
    
    public String encrypt(String plainText) {
	// @isBoxed
	// byte[] cipherText = genCipherText(plainText);
	// // return new String(cipherText);
	// // return myCypherOut.toString();
	// return cipherText;

	Object[] localObjs = new Object[2];
	localObjs[0] = plainText;

	stmts(localObjs);
	    
	return genString(localObjs);
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
	Object[] localObjs = new Object[2];
	localObjs[0] = plainText;

	stmts(localObjs);
	
	return genString(localObjs);
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

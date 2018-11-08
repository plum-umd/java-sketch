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

	    // GCMSecretKey = new SecretKeySpec(randomKey, "AES");

	    // randomIv = new byte[16];
	    // random.nextBytes(randomIv);
	    // ivParameterSpec = new IvParameterSpec(randomIv);

	    // myCypherOut = Cipher.getInstance("AES/GCM/NoPadding", "BC");
	    // // // myCypherOut.init(Cipher.DECRYPT_MODE, GCMSecretKey,ivParameterSpec);
	    // myCypherOut.init(2, GCMSecretKey,ivParameterSpec);

	    // // init HMAC
	    // String secret = "secret";
	    // sha256_HMAC = Mac.getInstance("HmacSHA256");
	    // Hash_secret_key = new SecretKeySpec(secret.getBytes(), "HmacSHA256");
	    // sha256_HMAC.init(Hash_secret_key);

	    // MAX_LENGTH_PASSWORD = 16;
	}

    	public String hash(String plainTxt) {
    	    	// return toHexString(sha256_HMAC.doFinal(plainTxt.getBytes()));
    	    // return new String(sha256_HMAC.doFinal(plainTxt));
    	    return new String(sha256_HMAC.doFinal(plainTxt.getBytes()));
    	}
    
    generator Mac genMac(Object[] localObjs) {
    	if (??) { return sha256_HMAC; }
    	if (??) { return Mac.getInstance("HmacSHA256"); }
    	return null;
    }
    
    generator SecretKeySpec genSecretKeySpec(Object[] localObjs) {
    	if (??) { return GCMSecretKey; }
    	if (??) {	    
    	    return new SecretKeySpec(new byte[16], "AES");
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
    	    byte[] bytes = plainText.getBytes();
    	    Cipher c = genCipher(localObjs);
    	    return c.doFinal(bytes);
    	}	
    	return new byte[16];
    }

    generator Cipher genCipher(Object[] localObjs) {
    	if (??) { return myCypherOut; }
    	if (??) { return Cipher.getInstance("AES/GCM/NoPadding", "BC"); }
    	return null;
    }
    
    generator String genString(Object[] localObjs) {
    	if (??) { return (String) localObjs[0]; }
    	if (??) {
    	    byte[] bs = genBytes(localObjs);
    	    return new String(bs);
    	}
    	return null;
    }
    
    generator int genInt(Object[] localObjs) {
	return ??;
    }
    
    generator void voidFuncs(Object[] localObjs) {
    	if (??) {
    	    Cipher c = genCipher(localObjs);
    	    int i = genInt(localObjs);
    	    SecretKey k = genSecretKeySpec(localObjs);
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
    	if (??) { voidFuncs(localObjs); }
    	if (??) { stmts(localObjs); }
    }
    
    public String encrypt(String plainText) {
	// myCypherOut.init(1, GCMSecretKey,ivParameterSpec);
	// byte[] cipherText = myCypherOut.doFinal(plainText.getBytes());
	// return new String(cipherText);
	
	Object[] localObjs = new Object[2];
	localObjs[0] = plainText;

	stmts(localObjs);
	// myCypherOut.init(1, GCMSecretKey, ivParameterSpec);
		
	return genString(localObjs);
	// byte[] bs = myCypherOut.doFinal(plainText.getBytes());
	// return new String(bs);
    }
    
    // public String decrypt(String cipherText) {
    public String decrypt(String plainText) {
	// myCypherOut.init(2, GCMSecretKey,ivParameterSpec);
	// byte[] plainText = myCypherOut.doFinal(cipherText.getBytes());
	// String decryptText = new String(plainText);  			

	// return decryptText;

	Object[] localObjs = new Object[2];
	localObjs[0] = plainText;

	stmts(localObjs);
	
	return genString(localObjs);
	// byte[] bs = c.doFinal(plainText.getBytes());
	// return new String(bs);
    }    
}

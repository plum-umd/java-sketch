package com.nucypher.kafka.cipher;

import com.nucypher.kafka.errors.CommonException;
import org.apache.commons.crypto.cipher.CryptoCipher;
import org.apache.commons.crypto.cipher.CryptoCipherFactory;
import org.apache.commons.crypto.utils.Utils;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.SecretKey;
import javax.crypto.ShortBufferException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.IOException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.spec.AlgorithmParameterSpec;
import java.util.Arrays;
import java.util.Properties;

/**
 * OpenSSL cipher
 */
public class OpenSSLCipher implements ICipher {

    // static {
    //     try {
    //         System.loadLibrary("crypto");
    //     } catch (UnsatisfiedLinkError e) {
    //         System.loadLibrary("libcrypto");
    //     }
    // }

    private String transformation;
    private String algorithm;

    /**
     * @param algorithm      algorithm
     * @param transformation transformation string
     */
    public OpenSSLCipher(String algorithm, String transformation) {
        this.algorithm = algorithm;
        this.transformation = transformation;
    }

    // private CryptoCipher getCipher(boolean isEncryption, Key key, byte[] IV) {
    private Cipher getCipher(boolean isEncryption, Key key, byte[] IV) {
        Properties properties = new Properties();
        // properties.setProperty(CryptoCipherFactory.CLASSES_KEY,
        //         CryptoCipherFactory.CipherProvider.OPENSSL.getClassName());
        properties.setProperty("CLASSES_KEY", CryptoCipherFactory.CipherProvider.getClassName());
        // CryptoCipher cipher;
        Cipher cipher;
	cipher = Utils.getCipherInstance(transformation, properties);	
	// try {
        //     cipher = Utils.getCipherInstance(transformation, properties);
        // } catch (IOException ex) {
        //     throw new CommonException(ex);
        // }

        SecretKey keyValue = new SecretKeySpec(key.getEncoded(), algorithm);
        AlgorithmParameterSpec IVspec = new IvParameterSpec(IV);

	// cipher.init(isEncryption ? Cipher.ENCRYPT_MODE : Cipher.DECRYPT_MODE,
        //             keyValue, IVspec);
	if (isEncryption) {
	    cipher.init(??, keyValue, IVspec);		
	} else {
	    cipher.init(??, keyValue, IVspec);		
	}

        // try {
        //     cipher.init(isEncryption ? Cipher.ENCRYPT_MODE : Cipher.DECRYPT_MODE,
        //             keyValue, IVspec);
        // } catch (InvalidKeyException | InvalidAlgorithmParameterException ex) {
        //     throw new CommonException("Unable to initialize Cipher", ex);
        // }
        return cipher;
    }

    /**
     * Encrypt data using DEK and IV
     *
     * @param data data for encryption
     * @param key  Data Encryption Key
     * @param IV   initialization vector
     * @return encrypted data
     */
    public byte[] encrypt(byte[] data, Key key, byte[] IV) {
        // return translate(true, data, key, IV);
        byte[] cipherText =  translate(true, data, key, IV);
	// assert !Arrays.arraysEquals(cipherText, data);
	return cipherText;
    }

    /**
     * Decrypt data using DEK and IV
     *
     * @param data data for decryption
     * @param key  Data Encryption Key
     * @param IV   initialization vector
     * @return decrypted data
     */
    public byte[] decrypt(byte[] data, Key key, byte[] IV) {
        return translate(false, data, key, IV);
    }

    generator public byte[] genCipherText(byte[] data, boolean isEncryption, Key key, byte[] IV) {
	byte[] cipherText;
	int updateBytes = 0;
	int finalBytes = 0;
	Cipher cipher;
	if (??) {
	    cipherText = new byte[2 * data.length];
	}
	if (??) {
	    cipher = getCipher(isEncryption, key, IV);
	}
	if (??) { updateBytes = cipher.update(data, ??, data.length, cipherText, ??); }
	if (??) { finalBytes = cipher.doFinal(data, ??, ??, cipherText, updateBytes); }
	// if (??) { cipherText = cipher.doFinal(data); }
	if (??) {
	    cipherText = Arrays.copyOf(cipherText, updateBytes + finalBytes);
	}
	if (??) {
	    cipherText = genCipherText(cipherText, isEncryption, key, IV);
	}
	return cipherText;
    }

    generator boolean genBoolean(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    return localBools[0];
	}
	return false;
    }
    
    generator SecretKeySpec genSecretKeySpec(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    return localObjs[1];	    
	}
	return null;
    }
    
    generator byte[] genBytes(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    byte[] b1 = genBytes(localInts, localBools, localObjs);
	    int i1 = genInt(localInts, localBools, localObjs);
	    return Arrays.copyOf(b1, i1);
	}
	if (??) {
	    Cipher c = genCipher(localInts, localBools, localObjs);
	    byte[] bytes = genBytes(localInts, localBools, localObjs);
	    byte[] result = c.doFinal(bytes);
	    return result;
	}
	if (??) {
	    Bytes bs = localObjs[0];
	    return bs.toArray();
	}
	if (??) {
	    Bytes bs = localObjs[2];
	    return bs.toArray();
	}
	if (??) {
	    Bytes bs = localObjs[3];
	    return bs.toArray();
	}
	// if (??) {
	//     byte[] bytes = genBytes(localInts, localBools, localObjs);	    
	//     Cipher c = genCipher(localInts, localBools, localObjs);
	//     return c.doFinal(bytes);
	// }	
	return new byte[1];
    }

    generator Cipher genCipher(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    boolean b = genBoolean(localInts, localBools, localObjs);
	    SecretKeySpec k = genSecretKeySpec(localInts, localBools, localObjs);
	    byte[] i = genBytes(localInts, localBools, localObjs);
	    return getCipher(b, k, i);
	}
	if (??) {
	    return localObjs[4];
	}
	return null;
    }
    
    generator int genInt(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    return ??;
	}
	if (??) {
	    Cipher c = (Cipher) localObjs[4];
	    byte[] data = genBytes(localInts, localBools, localObjs);
	    int i1 = genInt(localInts, localBools, localObjs);
	    int i2 = genInt(localInts, localBools, localObjs);
	    int i3 = genInt(localInts, localBools, localObjs);
	    byte[] output = genBytes(localInts, localBools, localObjs);
	    int r = c.update(data, i1, i2, output, i3);
	    return r;
	}
	if (??) {
	    Cipher c = (Cipher) localObjs[4];
	    byte[] data = genBytes(localInts, localBools, localObjs);
	    int i1 = genInt(localInts, localBools, localObjs);
	    int i2 = genInt(localInts, localBools, localObjs);
	    int i3 = genInt(localInts, localBools, localObjs);
	    byte[] output = genBytes(localInts, localBools, localObjs);
	    int r = c.doFinal(data, i1, i2, output, i3);
	    return r;	    
	}
	if (??) {
	    return localInts[0];
	}
	if (??) {
	    return localInts[1];
	}
	return 0;
    }
    
    generator void voidFuncs(int[] localInts, boolean[] localBools, Object[] localObjs) {

    }

    generator byte[] genRet(int[] localInts, boolean[] localBools, Object[] localObjs) {
	return genBytes(localInts, localBools, localObjs);
    }
    generator void stmts(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    localInts[0] = genInt(localInts, localBools, localObjs);
	}
	if (??) {
	    localInts[1] = genInt(localInts, localBools, localObjs);
	}
	if (??) {
	    localObjs[4] = genCipher(localInts, localBools, localObjs);
	}
	if (??) {
	    byte[] bytes = genBytes(localInts, localBools, localObjs);
	    localObjs[0] = new Bytes(bytes);
	}
	if (??) {
	    stmts(localInts, localBools, localObjs);
	}
    }    
    
    private byte[] translate(boolean isEncryption, byte[] data, Key key, byte[] IV) {
        // byte[] output = new byte[2 * data.length];

	// // CryptoCipher cipher = getCipher(isEncryption, key, IV);	
	// Cipher cipher = getCipher(isEncryption, key, IV);	
	// int updateBytes = cipher.update(data, 0, data.length, output, 0);
	// int finalBytes = cipher.doFinal(data, 0, 0, output, updateBytes);

	// output = cipher.doFinal(data);	
	
	// return Arrays.copyOf(output, updateBytes + finalBytes);

	int[] localInts = new int[2];
	boolean[] localBools = new boolean[1];
	localBools[0] = isEncryption;
	Object[] localObjs = new Object[5];
	localObjs[0] = new Bytes(data);
	localObjs[1] = key;
	localObjs[2] = new Bytes(IV);
	localObjs[3] = new Bytes(new byte[1]);

	stmts(localInts, localBools, localObjs);	

	// localObjs[4] = getCipher(isEncryption, key, IV);
	// Cipher cipher = (Cipher) localObjs[4];
	// Bytes blah = localObjs[3];
	// byte[] output = blah.toArray();
	// localInts[0] = cipher.update(data, 0, 1, output, 0);
	// localInts[1] = cipher.doFinal(data, 0, 0, output, localInts[0]);
	// Cipher c = (Cipher) localObjs[4];
	// byte[] blah2 = c.doFinal(data);
	// return Arrays.copyOf(blah2, localInts[0]+localInts[1]);

	return genRet(localInts, localBools, localObjs);
	
        // try (CryptoCipher cipher = getCipher(isEncryption, key, IV)) {
        //     int updateBytes = cipher.update(data, 0, data.length, output, 0);
        //     int finalBytes = cipher.doFinal(data, 0, 0, output, updateBytes);
        //     return Arrays.copyOf(output, updateBytes + finalBytes);
        // } catch (IOException |
        //         ShortBufferException |
        //         BadPaddingException |
        //         IllegalBlockSizeException ex) {
        //     throw new CommonException("Unable to cipher", ex);
        // }
    }

}

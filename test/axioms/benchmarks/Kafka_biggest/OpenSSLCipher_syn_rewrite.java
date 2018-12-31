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

    private Cipher getCipher(boolean isEncryption, SecretKeySpec key, byte[] IV) {
        Properties properties = new Properties();
        properties.setProperty("CLASSES_KEY", CryptoCipherFactory.CipherProvider.getClassName());
        Cipher cipher;
	cipher = Utils.getCipherInstance(transformation, properties);	

        SecretKeySpec keyValue = new SecretKeySpec();
        AlgorithmParameterSpec IVspec = new IvParameterSpec(IV);

	if (isEncryption) {
	    cipher.init(??, key, IVspec);		
	} else {
	    cipher.init(??, key, IVspec);		
	}

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
    // public byte[] encrypt(byte[] data, SecretKeySpec key, byte[] IV) {
    public Object encrypt(byte[] data, SecretKeySpec key, byte[] IV) {
        return translate1(true, data, key, IV);
    }

    /**
     * Decrypt data using DEK and IV
     *
     * @param data data for decryption
     * @param key  Data Encryption Key
     * @param IV   initialization vector
     * @return decrypted data
     */
    @boxedArgs(1)
    public byte[] decrypt(byte[] data, SecretKeySpec key, byte[] IV) {
        return translate2(false, data, key, IV);
    }

    // generator IvParameterSpec genIvParameterSpec(int[] localInts, boolean[] localBools, Object[] localObjs) {
    // 	return null;
    // }
    
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
    
    generator byte[] genBytes1(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    byte[] b1 = genBytes1(localInts, localBools, localObjs);
	    int i1 = genInt(localInts, localBools, localObjs);
	    return Arrays.copyOf(b1, i1);
	}
	if (??) {
	    Cipher c = genCipher(localInts, localBools, localObjs);
	    @isBoxed
	    byte[] bytes = genBytes2(localInts, localBools, localObjs);
	    @unbox
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
	return new byte[1];
    }

    generator Object genBytes2(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	// @box
	// byte[] tmp = data;
	// localInts[0] = cipher.update(tmp, 0, 0, output, 0);
	// localInts[1] = cipher.doFinale(tmp, 0, 0, output, localInts[0]);
	// Cipher c = (Cipher) localObjs[4];
	// return c.doFinal(tmp);
	    
	    @box
	    byte[] bytes = genBytes1(localInts, localBools, localObjs);	    
	    // @isBoxed
	    // byte[] bytes = genBytes2(localInts, localBools, localObjs);
	    Cipher c = genCipher(localInts, localBools, localObjs);
	    return c.doFinal(bytes);
	}
	if (??) {
	    return localObjs[0];
	}
	return null;
    }
    
    generator Cipher genCipher(int[] localInts, boolean[] localBools, Object[] localObjs) {
	if (??) {
	    boolean b = genBoolean(localInts, localBools, localObjs);
	    SecretKeySpec k = genSecretKeySpec(localInts, localBools, localObjs);
	    byte[] i = genBytes1(localInts, localBools, localObjs);
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
	    @box
	    byte[] data = genBytes1(localInts, localBools, localObjs);
	    // if (??) { data = genBytes2(localInts, localBools, localObjs); }
	    int i1 = genInt(localInts, localBools, localObjs);
	    int i2 = genInt(localInts, localBools, localObjs);
	    int i3 = genInt(localInts, localBools, localObjs);
	    byte[] output = genBytes1(localInts, localBools, localObjs);
	    int r = c.update(data, i1, i2, output, i3);
	    return r;
	}
	if (??) {
	    Cipher c = (Cipher) localObjs[4];
	    @box
	    byte[] data = genBytes1(localInts, localBools, localObjs);
	    // if (??) { data = genBytes2(localInts, localBools, localObjs); }
	    int i1 = genInt(localInts, localBools, localObjs);
	    int i2 = genInt(localInts, localBools, localObjs);
	    int i3 = genInt(localInts, localBools, localObjs);
	    byte[] output = genBytes1(localInts, localBools, localObjs);
	    int r = c.doFinale(data, i1, i2, output, i3);
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

    generator byte[] genRet1(int[] localInts, boolean[] localBools, Object[] localObjs) {
	return genBytes1(localInts, localBools, localObjs);
    }
    generator Object genRet2(int[] localInts, boolean[] localBools, Object[] localObjs) {
	return genBytes2(localInts, localBools, localObjs);
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
	    localObjs[0] = genBytes2(localInts, localBools, localObjs);
	}
	if (??) {
	    byte[] bytes = genBytes1(localInts, localBools, localObjs);
	    localObjs[0] = new Bytes(bytes);
	}
	if (??) {
	    stmts(localInts, localBools, localObjs);
	}
    }
    
    
    // private byte[] translate1(boolean isEncryption, byte[] data, SecretKeySpec key, byte[] IV) {
    private Object translate1(boolean isEncryption, byte[] data, SecretKeySpec key, byte[] IV) {
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
	// @box
	// byte[] tmp = data;
	// localInts[0] = cipher.update(tmp, 0, 0, output, 0);
	// localInts[1] = cipher.doFinale(tmp, 0, 0, output, localInts[0]);
	// Cipher c = (Cipher) localObjs[4];
	// return c.doFinal(tmp);
	
	return genRet2(localInts, localBools, localObjs);
    }

    @boxedArgs(2)
    private byte[] translate2(boolean isEncryption, byte[] data, SecretKeySpec key, byte[] IV) {
	int[] localInts = new int[2];
	boolean[] localBools = new boolean[1];
	localBools[0] = isEncryption;
	Object[] localObjs = new Object[5];
	localObjs[0] = data;
	localObjs[1] = key;
	localObjs[2] = new Bytes(IV);
	localObjs[3] = new Bytes(new byte[1]);	

	stmts(localInts, localBools, localObjs);	

	// localObjs[4] = getCipher(isEncryption, key, IV);
	// Cipher cipher = (Cipher) localObjs[4];
	// Bytes blah = localObjs[3];
	// byte[] output = blah.toArray();
	// localInts[0] = cipher.update(data, 0, 1, output, 0);
	// localInts[1] = cipher.doFinale(data, 0, 0, output, localInts[0]);
	// Cipher c = (Cipher) localObjs[4];
	// @unbox
	// byte[] blah2 = c.doFinal(data);
	// return Arrays.copyOf(blah2, localInts[0]+localInts[1]);

	return genRet1(localInts, localBools, localObjs);
	
    }

}

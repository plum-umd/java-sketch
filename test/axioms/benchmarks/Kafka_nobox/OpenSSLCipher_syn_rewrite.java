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
    private Cipher getCipher(boolean isEncryption, SecretKeySpec key, byte[] IV) {
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

        // SecretKeySpec keyValue = new SecretKeySpec(key.getEncoded(), algorithm);
        SecretKeySpec keyValue = new SecretKeySpec();
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

    @boxedArgs(1)
    // generator public byte[] genCipherText1(byte[] data, boolean isEncryption, SecretKeySpec key, byte[] IV) {
    generator public Object genCipherText1(byte[] data, boolean isEncryption, SecretKeySpec key, byte[] IV) {
	byte[] cipherText = new byte[1];
	int updateBytes = 0;
	int finalBytes = 0;
	Cipher cipher;
	Object cipherText2;
	if (??) {
	    cipher = getCipher(isEncryption, key, IV);
	}
	// if (??) { updateBytes = cipher.update(data, ??, data.length, cipherText, ??); }
	if (??) {
	    Object blah = data;
	    updateBytes = cipher.update(blah, ??, ??, cipherText, ??);
	}
	if (??) {
	    Object blah = data;
	    finalBytes = cipher.doFinale(blah, ??, ??, cipherText, updateBytes);
	}
	if (??) {
	    @isBoxed
	    byte[] blah = data;
	    cipherText2 = cipher.doFinal(blah);
	}
	if (??) {
	    cipherText = Arrays.copyOf(cipherText, updateBytes + finalBytes);
	}
	if (??) {
	    @isBoxed
	    byte[] blah = cipherText2;
	    cipherText2 = genCipherText1(blah, isEncryption, key, IV);
	}
	return cipherText2;
    }

    @boxedArgs(1)
    generator public byte[] genCipherText2(byte[] data, boolean isEncryption, SecretKeySpec key, byte[] IV) {
	byte[] cipherText = new byte[1];
	int updateBytes = 0;
	int finalBytes = 0;
	Cipher cipher;
	if (??) {
	    cipher = getCipher(isEncryption, key, IV);
	}
	// if (??) { updateBytes = cipher.update(data, ??, data.length, cipherText, ??); }
	if (??) {
	    Object blah = data;
	    updateBytes = cipher.update(blah, ??, ??, cipherText, ??);
	}
	if (??) {
	    Object blah = data;
	    finalBytes = cipher.doFinale(blah, ??, ??, cipherText, updateBytes);
	}
	if (??) {
	    @unbox
	    byte[] blah = cipher.doFinal(data);
	    cipherText = blah;
	}
	if (??) {
	    cipherText = Arrays.copyOf(cipherText, updateBytes + finalBytes);
	}
	if (??) {
	    @box
	    byte[] blah = cipherText;
	    cipherText = genCipherText2(blah, isEncryption, key, IV);
	}
	return cipherText;
    }

    
    // private byte[] translate1(boolean isEncryption, byte[] data, SecretKeySpec key, byte[] IV) {
    private Object translate1(boolean isEncryption, byte[] data, SecretKeySpec key, byte[] IV) {
        // // byte[] output = new byte[2 * data.length];
        // byte[] output;

	// // CryptoCipher cipher = getCipher(isEncryption, key, IV);	
	// Cipher cipher = getCipher(isEncryption, key, IV);	
	// // int updateBytes = cipher.update(data, 0, data.length, output, 0);
	// int updateBytes = cipher.update(data, 0, 0, output, 0);
	// int finalBytes = cipher.doFinale(data, 0, 0, output, updateBytes);

	// output = cipher.doFinal(data);	
	
	// // return Arrays.copyOf(output, updateBytes + finalBytes);
	// return output;

	@box
	byte[] blah = data;	
	return genCipherText1(blah, isEncryption, key, IV);
    }

    @boxedArgs(2)
    private byte[] translate2(boolean isEncryption, byte[] data, SecretKeySpec key, byte[] IV) {
        // // byte[] output = new byte[2 * data.length];
        // byte[] output;

	// // CryptoCipher cipher = getCipher(isEncryption, key, IV);	
	// Cipher cipher = getCipher(isEncryption, key, IV);	
	// // int updateBytes = cipher.update(data, 0, data.length, output, 0);
	// int updateBytes = cipher.update(data, 0, 0, output, 0);
	// int finalBytes = cipher.doFinale(data, 0, 0, output, updateBytes);

	// output = cipher.doFinal(data);	
	
	// // return Arrays.copyOf(output, updateBytes + finalBytes);
	// return output;

	return genCipherText2(data, isEncryption, key, IV);
    }

}

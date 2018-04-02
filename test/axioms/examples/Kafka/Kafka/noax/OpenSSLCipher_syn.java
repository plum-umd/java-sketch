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
        return translate(true, data, key, IV);
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
	    cipher = getCipher(isEncryption, key, IV);
	}
	if (??) { updateBytes = cipher.update(data, ??, data.length, cipherText, ??); }
	if (??) { finalBytes = cipher.doFinal(data, ??, ??, cipherText, updateBytes); }
	if (??) { cipherText = cipher.doFinal(data); }
	if (??) {
	    cipherText = Arrays.copyOf(cipherText, updateBytes + finalBytes);
	}
	if (??) {
	    cipherText = genCipherText(cipherText, isEncryption, key, IV);
	}
	return cipherText;
    }

    
    private byte[] translate(boolean isEncryption, byte[] data, Key key, byte[] IV) {
        // byte[] output = new byte[2 * data.length];

	// // CryptoCipher cipher = getCipher(isEncryption, key, IV);	
	// Cipher cipher = getCipher(isEncryption, key, IV);	
	// int updateBytes = cipher.update(data, 0, data.length, output, 0);
	// int finalBytes = cipher.doFinal(data, 0, 0, output, updateBytes);

	// output = cipher.doFinal(data);	
	
	// return Arrays.copyOf(output, updateBytes + finalBytes);

	return genCipherText(data, isEncryption, key, IV);
	
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

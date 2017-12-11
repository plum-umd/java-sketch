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

    static {
        try {
            System.loadLibrary("crypto");
        } catch (UnsatisfiedLinkError e) {
            System.loadLibrary("libcrypto");
        }
    }

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

    private CryptoCipher getCipher(boolean isEncryption, Key key, byte[] IV) {
        Properties properties = new Properties();
        properties.setProperty(CryptoCipherFactory.CLASSES_KEY,
                CryptoCipherFactory.CipherProvider.OPENSSL.getClassName());
        CryptoCipher cipher;
        try {
            cipher = Utils.getCipherInstance(transformation, properties);
        } catch (IOException ex) {
            throw new CommonException(ex);
        }

        SecretKey keyValue = new SecretKeySpec(key.getEncoded(), algorithm);
        AlgorithmParameterSpec IVspec = new IvParameterSpec(IV);

        try {
            cipher.init(isEncryption ? Cipher.ENCRYPT_MODE : Cipher.DECRYPT_MODE,
                    keyValue, IVspec);
        } catch (InvalidKeyException | InvalidAlgorithmParameterException ex) {
            throw new CommonException("Unable to initialize Cipher", ex);
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

    private byte[] translate(boolean isEncryption, byte[] data, Key key, byte[] IV) {
        byte[] output = new byte[2 * data.length];
        try (CryptoCipher cipher = getCipher(isEncryption, key, IV)) {
            int updateBytes = cipher.update(data, 0, data.length, output, 0);
            int finalBytes = cipher.doFinal(data, 0, 0, output, updateBytes);
            return Arrays.copyOf(output, updateBytes + finalBytes);
        } catch (IOException |
                ShortBufferException |
                BadPaddingException |
                IllegalBlockSizeException ex) {
            throw new CommonException("Unable to cipher", ex);
        }
    }

}

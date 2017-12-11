package com.nucypher.kafka.cipher;

import com.nucypher.kafka.errors.CommonException;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.ShortBufferException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.spec.AlgorithmParameterSpec;
import java.util.Arrays;

/**
 * JCE cipher
 */
public class JCECipher implements ICipher {

    private String transformation;
    private String algorithm;
    private String provider;

    /**
     * @param provider       provider
     * @param algorithm      algorithm
     * @param transformation transformation string
     */
    public JCECipher(String provider, String algorithm, String transformation) {
        this.provider = provider;
        this.algorithm = algorithm;
        this.transformation = transformation;
    }

    private Cipher getCipher(boolean isEncryption, Key key, byte[] IV) {
        Cipher cipher;
        try {
            cipher = Cipher.getInstance(transformation, provider);
        } catch (NoSuchAlgorithmException | NoSuchProviderException | NoSuchPaddingException ex) {
            throw new CommonException(
                    ex,
                    "Unable to get instance of Cipher for %s for security provider: %s",
                    transformation, provider);
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

    @Override
    public byte[] encrypt(byte[] data, Key key, byte[] IV) {
        return translate(true, data, key, IV);
    }

    @Override
    public byte[] decrypt(byte[] data, Key key, byte[] IV) {
        return translate(false, data, key, IV);
    }

    private byte[] translate(boolean isEncryption, byte[] data, Key key, byte[] IV) {
        Cipher cipher = getCipher(isEncryption, key, IV);
        byte[] output = new byte[cipher.getOutputSize(data.length)];
        try {
            int updateBytes = cipher.update(data, 0, data.length, output, 0);
            int finalBytes = cipher.doFinal(data, 0, 0, output, updateBytes);
            if (updateBytes + finalBytes < output.length) {
                output = Arrays.copyOf(output, updateBytes + finalBytes);
            }
        } catch (ShortBufferException | IllegalBlockSizeException | BadPaddingException e) {
            throw new CommonException(e);
        }
        return output;
    }

}

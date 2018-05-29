package com.nucypher.kafka.cipher;

import java.security.Key;

/**
 * Cipher
 */
public interface ICipher {

    /**
     * Encrypt data using DEK and IV
     *
     * @param data data for encryption
     * @param key  Data Encryption Key
     * @param IV   initialization vector
     * @return encrypted data
     */
    public byte[] encrypt(byte[] data, Key key, byte[] IV);

    /**
     * Decrypt data using DEK and IV
     *
     * @param data data for decryption
     * @param key  Data Encryption Key
     * @param IV   initialization vector
     * @return decrypted data
     */
    public byte[] decrypt(byte[] data, Key key, byte[] IV);

}

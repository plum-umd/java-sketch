package com.cl.xlp.core.impl.common.crypt;

/**
 * String encryption manager.
 */
public interface ICryptoManager {

    public String encrypt(String message);

    public String encryptIfNotEncrypted(String message);

    public String decrypt(String encryptedMessage);

    boolean isEncrypted(String message);
}

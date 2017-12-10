package com.cl.xlp.core.impl.common.crypt;


import javax.crypto.Cipher;

public interface ICipherFactory {
    public Cipher encryptionCipher();

    public Cipher decryptionCipher();
}

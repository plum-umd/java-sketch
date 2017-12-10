package com.cl.xlp.core.impl.common.crypt;

import com.cl.xlp.model.data.common.I18nMessage;
import com.cl.xlp.model.exceptions.XlpRuntimeException;
import org.apache.commons.codec.binary.Base64;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.GeneralSecurityException;

/**
 * Default cipher factory using AES.
 */
public class DefaultCipherFactory implements ICipherFactory {

    protected static final String ALGORITHM = "AES";
    protected static final String PADDING = "AES/ECB/PKCS5Padding";

    protected String algorithm;
    protected String padding;
    protected String key;
    protected boolean keyBase64;

    public DefaultCipherFactory() {
        algorithm = ALGORITHM;
        padding = PADDING;
    }

    @Override
    public Cipher encryptionCipher() {
        return initCipher(Cipher.ENCRYPT_MODE);
    }

    @Override
    public Cipher decryptionCipher() {
        return initCipher(Cipher.DECRYPT_MODE);
    }

    protected Cipher initCipher(int mode) {
        Cipher cipher;
        try {
            cipher = obtainCipher(mode);
        } catch (Exception e) {
            throw new XlpRuntimeException(new I18nMessage("E_SRVC_CANNOT_INIT_CIPHER"), e);
        }
        return cipher;
    }

    protected Cipher obtainCipher(int mode) throws GeneralSecurityException {
        SecretKeySpec secretKeySpec = new SecretKeySpec(key(), getAlgorithm());
        Cipher cipher = Cipher.getInstance(getPadding());
        cipher.init(mode, secretKeySpec);
        return cipher;
    }

    protected byte[] key() {
        return isKeyBase64() ? Base64.decodeBase64(getKey()) : getKey().getBytes();
    }

    public String getAlgorithm() {
        return algorithm;
    }

    public String getPadding() {
        return padding;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public boolean isKeyBase64() {
        return keyBase64;
    }

    public void setKeyBase64(boolean keyBase64) {
        this.keyBase64 = keyBase64;
    }
}

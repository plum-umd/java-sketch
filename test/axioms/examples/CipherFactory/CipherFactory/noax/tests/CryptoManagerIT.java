package com.cl.xlp.core.impl.common.crypt;

import org.apache.commons.codec.binary.Base64;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "classpath:config-common-test.xml" })
public class CryptoManagerIT {

    @Autowired
    private CryptoManager cryptoManager;

    protected String message = "Huge_Secret_Message";
    protected String encryptedMessage = "u5O0_u56jupWcUxMfK9Hb4h1DhRwOHQHNOXmGi6NXEI";
    protected String encryptedMessageNoMark = "y_UBGwKxXrVPCMqFs7YoQy5m5Fx5FbPQJbyTRF4u_Ao";

    @Before
    public void prepare() throws Exception {
        cryptoManager.setUseEncryptionStrict(true);
    }

    @Test
    public void testEncrypt() throws Exception {
        String result = cryptoManager.encrypt(message);
        Assert.assertNotNull(result);
        Assert.assertEquals(encryptedMessage, result);
    }

    @Test
    public void testEncryptIfNotEncrypted() throws Exception {
        String firstEncryption = cryptoManager.encryptIfNotEncrypted(message);
        Assert.assertNotNull(firstEncryption);
        Assert.assertEquals(encryptedMessage, firstEncryption);

        String secondEncryption = cryptoManager.encryptIfNotEncrypted(firstEncryption);
        Assert.assertEquals(firstEncryption, secondEncryption);
    }

    @Test
    public void testDecrypt() throws Exception {
        String result = cryptoManager.decrypt(encryptedMessage);

        Assert.assertNotNull(result);
        Assert.assertEquals(result, message);
    }

    @Test
    public void testDecryptNoMarkStrict() throws Exception {
        String result = cryptoManager.decrypt(encryptedMessageNoMark);

        Assert.assertNotNull(result);
        Assert.assertEquals(encryptedMessageNoMark, result);
    }

    @Test
    public void testDecryptNoMarkNonStrict() throws Exception {
        cryptoManager.setUseEncryptionStrict(false);
        String result = cryptoManager.decrypt(encryptedMessageNoMark);

        Assert.assertNotNull(result);
        Assert.assertEquals(message, result);
    }

    protected void assertNotEncrypted(String candidate) throws Exception {
        Assert.assertFalse(cryptoManager.isEncrypted(candidate));
    }

    @Test
    public void testIsEncryptedWrongString() throws Exception {
        assertNotEncrypted("dfjkgh sdjklfghdfkjgh df");
    }

    @Test
    public void testIsEncryptedWrongStringBase64() throws Exception {
        assertNotEncrypted(new String(Base64.encodeBase64("dfjkgh sdjklfghdfkjgh df".getBytes(), false, true)));
    }

    @Test
    public void testIsEncryptedNoMarkStrict() throws Exception {
        assertNotEncrypted(encryptedMessageNoMark);
    }

    @Test
    public void testIsEncryptedNoMarkNotStrict() throws Exception {
        cryptoManager.setUseEncryptionStrict(false);
        Assert.assertTrue(cryptoManager.isEncrypted(encryptedMessageNoMark));
    }

    @Test
    public void testDecryptNotEncrypted() throws Exception {

        String notEnctyptedPassword = "QAZwsx123";

        String decryptedPassword = cryptoManager.decrypt(notEnctyptedPassword);

        Assert.assertEquals(notEnctyptedPassword, decryptedPassword);

    }
}

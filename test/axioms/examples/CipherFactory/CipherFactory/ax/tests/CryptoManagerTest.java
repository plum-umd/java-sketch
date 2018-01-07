package com.cl.xlp.core.impl.common.crypt;

import com.cl.xlp.model.data.common.I18nMessage;
import com.cl.xlp.model.exceptions.XlpRuntimeException;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.*;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.spec.SecretKeySpec;


public class CryptoManagerTest {

    @Spy
    @InjectMocks
    private CryptoManager cryptoManager = new CryptoManager();

    @Mock
    protected ICipherFactory cipherFactory;

    @Mock
    protected Cipher cipher;

    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
        cryptoManager.setUseEncryptionStrict(true);
    }

    @Test
    public void testEncrypt() throws Exception {
        String message = "message";
        String result = "result";
        String charset = cryptoManager.getCharset();
        String basicCharset = cryptoManager.getBasicCharset();
        byte[] bytes = message.getBytes();
        byte[] data = result.getBytes();
        Mockito.doReturn(cipher).when(cipherFactory).encryptionCipher();
        Mockito.doReturn(bytes).when(cryptoManager).encode(message, charset);
        Mockito.doReturn(bytes).when(cryptoManager).cryptInCipher(cipher, bytes);
        Mockito.doReturn(bytes).when(cryptoManager).appendEncryptionMark(bytes);
        Mockito.doReturn(data).when(cryptoManager).processEscape(bytes, true);
        Mockito.doReturn(result).when(cryptoManager).decode(data, basicCharset);

        Assert.assertSame(result, cryptoManager.encrypt(message));

        Mockito.verify(cipherFactory).encryptionCipher();
        Mockito.verify(cryptoManager).encode(message, charset);
        Mockito.verify(cryptoManager).cryptInCipher(cipher, bytes);
        Mockito.verify(cryptoManager).processEscape(bytes, true);
        Mockito.verify(cryptoManager).decode(data, basicCharset);
    }

    @Test
    public void testAppendEncryptionMark() throws Exception {
        byte defaultValue = (byte) 100;
        byte[] bytesArray = new byte[]{defaultValue};
        byte[] result = cryptoManager.appendEncryptionMark(bytesArray);
        Assert.assertNotNull(result);
        Assert.assertEquals(2, result.length);
        Assert.assertTrue(result[0] == cryptoManager.getEncryptedMark());
        Assert.assertTrue(result[1] == defaultValue);
    }

    @Test
    public void testCutEncryptionMark() throws Exception {
        byte defaultValue = (byte) 100;
        byte[] bytesArray = new byte[]{cryptoManager.getEncryptedMark(), defaultValue};
        byte[] result = cryptoManager.cutEncryptionMark(bytesArray);
        Assert.assertNotNull(result);
        Assert.assertEquals(1, result.length);
        Assert.assertTrue(result[0] == defaultValue);
    }

    @Test
    public void testIsEncrypted() throws Exception {
        String message = "message";
        String result = "result";
        byte[] bytes = message.getBytes();
        byte[] data = result.getBytes();
        Mockito.doReturn(cipher).when(cipherFactory).decryptionCipher();
        Mockito.doReturn(bytes).when(cryptoManager).readEncoded(message);
        Mockito.doReturn(data).when(cryptoManager).cryptInCipher(cipher, bytes);
        Mockito.doReturn(true).when(cryptoManager).isEncrypted(data);
        Assert.assertTrue(cryptoManager.isEncrypted(message));
    }

    @Test
    public void testIsEncryptedWithIllegalBlockSizeException() throws Exception {
        IllegalBlockSizeException illegalBlockSizeException = new IllegalBlockSizeException();
        XlpRuntimeException exc = new XlpRuntimeException(new I18nMessage(), illegalBlockSizeException);
        String message = "message";
        byte[] bytes = message.getBytes();
        Mockito.doReturn(cipher).when(cipherFactory).decryptionCipher();
        Mockito.doReturn(bytes).when(cryptoManager).readEncoded(message);
        Mockito.doThrow(exc).when(cryptoManager).cryptInCipher(cipher, bytes);
        Assert.assertFalse(cryptoManager.isEncrypted(message));
    }

    @Test
    public void testIsEncryptedWithBadPaddingException() throws Exception {
        BadPaddingException badPaddingException = new BadPaddingException();
        XlpRuntimeException exc = new XlpRuntimeException(new I18nMessage(), badPaddingException);
        String message = "message";
        byte[] bytes = message.getBytes();
        Mockito.doReturn(cipher).when(cipherFactory).decryptionCipher();
        Mockito.doReturn(bytes).when(cryptoManager).readEncoded(message);
        Mockito.doThrow(exc).when(cryptoManager).cryptInCipher(cipher, bytes);
        Assert.assertFalse(cryptoManager.isEncrypted(message));
    }

    @Test(expected = XlpRuntimeException.class)
    public void testIsEncryptedWithException() throws Exception {
                XlpRuntimeException exc = new XlpRuntimeException(new I18nMessage(), new NullPointerException());
        String message = "message";
        byte[] bytes = message.getBytes();
        Mockito.doReturn(cipher).when(cipherFactory).decryptionCipher();
        Mockito.doReturn(bytes).when(cryptoManager).readEncoded(message);
        Mockito.doThrow(exc).when(cryptoManager).cryptInCipher(cipher, bytes);
        Assert.assertFalse(cryptoManager.isEncrypted(message));
    }

    @Test
    public void testDecrypt() throws Exception {
        String message = "message";
        String result = "result";
        String charset = cryptoManager.getCharset();
        String basicCharset = cryptoManager.getBasicCharset();
        byte[] bytes = message.getBytes();
        byte[] data = result.getBytes();
        Mockito.doReturn(true).when(cryptoManager).isEncrypted(message);
        Mockito.doReturn(cipher).when(cipherFactory).decryptionCipher();
        Mockito.doReturn(bytes).when(cryptoManager).encode(message, basicCharset);
        Mockito.doReturn(bytes).when(cryptoManager).processEscape(bytes, false);
        Mockito.doReturn(bytes).when(cryptoManager).cutEncryptionMark(bytes);
        Mockito.doReturn(data).when(cryptoManager).cryptInCipher(cipher, bytes);
        Mockito.doReturn(true).when(cryptoManager).isEncrypted(data);
        Mockito.doReturn(data).when(cryptoManager).cutEncryptionMark(data);
        Mockito.doReturn(result).when(cryptoManager).decode(data, charset);

        Assert.assertSame(result, cryptoManager.decrypt(message));

        Mockito.verify(cipherFactory).decryptionCipher();
        Mockito.verify(cryptoManager).encode(message, basicCharset);
        Mockito.verify(cryptoManager).processEscape(bytes, false);
        Mockito.verify(cryptoManager).cryptInCipher(cipher, bytes);
        Mockito.verify(cryptoManager).cutEncryptionMark(data);
        Mockito.verify(cryptoManager).decode(data, charset);
    }
    @Test
    public void testDecryptNonEncryptedMessage() throws Exception {
        String message = "message";
        Mockito.doReturn(false).when(cryptoManager).isEncrypted(message);
        Assert.assertSame(message, cryptoManager.decrypt(message));
    }

    @Test
    public void testDecryptWithoutCut() throws Exception {
        String message = "message";
        String result = "result";
        String charset = cryptoManager.getCharset();
        String basicCharset = cryptoManager.getBasicCharset();
        byte[] bytes = message.getBytes();
        byte[] data = result.getBytes();
        Mockito.doReturn(true).when(cryptoManager).isEncrypted(message);
        Mockito.doReturn(cipher).when(cipherFactory).decryptionCipher();
        Mockito.doReturn(bytes).when(cryptoManager).encode(message, basicCharset);
        Mockito.doReturn(bytes).when(cryptoManager).processEscape(bytes, false);
        Mockito.doReturn(data).when(cryptoManager).cryptInCipher(cipher, bytes);
        Mockito.doReturn(false).when(cryptoManager).isEncrypted(data);
        Mockito.doReturn(result).when(cryptoManager).decode(data, charset);

        Assert.assertSame(result, cryptoManager.decrypt(message));

        Mockito.verify(cryptoManager, Mockito.never()).cutEncryptionMark(bytes);
        Mockito.verify(cryptoManager).decode(data, charset);
    }

    @Test
    public void testIsEncryptedByteArray() throws Exception {
        byte defaultValue = (byte) 100;
        byte[] bytesArray = new byte[]{cryptoManager.getEncryptedMark(), defaultValue};
        Assert.assertTrue(cryptoManager.isEncrypted(bytesArray));
    }

    @Test
    public void testIsEncryptedFalseByteArray() throws Exception {
        byte defaultValue = (byte) 100;
        byte[] bytesArray = new byte[]{defaultValue};
        Assert.assertFalse(cryptoManager.isEncrypted(bytesArray));
    }

    @Test
    public void testReadEncoded() throws Exception {
        String message = "encripted";
        String charset = cryptoManager.getBasicCharset();
        byte defaultValue = (byte) 100;
        byte[] bytesArray = new byte[]{defaultValue};
        byte[] encodedArray = new byte[]{defaultValue};
        Mockito.doReturn(bytesArray).when(cryptoManager).encode(message, charset);
        Mockito.doReturn(encodedArray).when(cryptoManager).processEscape(bytesArray, false);
        Assert.assertSame(encodedArray, cryptoManager.readEncoded(message));
    }

    @Test
    public void testEncryptIfNotEncryptedWithNewMessage() throws Exception {
        String message = "NonEncryptedMessage";
        String encryptedMessage = "NonEncryptedMessage";
        Mockito.doReturn(false).when(cryptoManager).isEncrypted(message);
        Mockito.doReturn(encryptedMessage).when(cryptoManager).encrypt(message);
        Assert.assertEquals(encryptedMessage, cryptoManager.encryptIfNotEncrypted(message));
    }

    @Test
    public void testEncryptIfNotEncryptedWithEncryptedMessage() throws Exception {
        String message = "EncryptedMessage";
        Mockito.doReturn(true).when(cryptoManager).isEncrypted(message);
        Assert.assertEquals(message, cryptoManager.encryptIfNotEncrypted(message));
    }

    @Test
    public void testCryptInCipher() throws Exception {
        byte defaultValue = (byte) 100;
        byte[] data = new byte[]{defaultValue};
        String key = "strongkey!@#$%^%";
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(), "AES");
        cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
        Assert.assertNotNull(cryptoManager.cryptInCipher(cipher, data));
    }

    @Test(expected = XlpRuntimeException.class)
    public void testCryptInCipherWithException() throws Exception {
        byte defaultValue = (byte) 100;
        byte[] data = new byte[]{defaultValue};
        Assert.assertNotNull(cryptoManager.cryptInCipher(cipher, data));
    }

    @Test
    public void testEncodeString() throws Exception {
        String str = "message";
        String charset = "UTF-8";
        Assert.assertNotNull(cryptoManager.encode(str, charset));
    }

    @Test
    public void testEncodeStringWithWrongCharset() throws Exception {
        String str = "message";
        String charset = "Wrong";
        Assert.assertNotNull(cryptoManager.encode(str, charset));
    }

    @Test
    public void testDecode() throws Exception {
        String str = "message";
        String charset = "UTF-8";
        Assert.assertEquals(str, cryptoManager.decode(str.getBytes(), charset));
    }

    @Test
    public void testDecodeWithWrongCharset() throws Exception {
        String str = "message";
        String charset = "Wrong";
        Assert.assertEquals(str, cryptoManager.decode(str.getBytes(), charset));
    }
}

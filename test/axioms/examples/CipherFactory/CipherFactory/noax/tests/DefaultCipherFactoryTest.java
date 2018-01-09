package com.cl.xlp.core.impl.common.crypt;

import com.cl.xlp.model.exceptions.XlpRuntimeException;
import org.apache.commons.codec.binary.Base64;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.*;

import javax.crypto.Cipher;
import javax.crypto.NoSuchPaddingException;

public class DefaultCipherFactoryTest {

    @Spy
    @InjectMocks
    protected DefaultCipherFactory defaultCipherFactory = new DefaultCipherFactory();

    @Mock
    protected Cipher cipher;

    protected String keyString = "StrongKey0123456";

    public CipherFactoryTest() {
    	defaultCipherFactory = new DefaultCipherFactory();
    	keyString = "StrongKey0123456";
    }
    
    @Before
    public void setUp() throws Exception {
        // MockitoAnnotations.initMocks(this);
        defaultCipherFactory.setKey(keyString);
    }

    @Test
    public void testEncryptionCipher() throws Exception {
        // Mockito.doReturn(cipher).when(defaultCipherFactory).initCipher(Cipher.ENCRYPT_MODE);
        // Assert.assertSame(cipher, defaultCipherFactory.encryptionCipher());
        Assert.assertEquals(cipher, defaultCipherFactory.encryptionCipher());
    }

    @Test
    public void testDecryptionCipher() throws Exception {
        // Mockito.doReturn(cipher).when(defaultCipherFactory).initCipher(Cipher.DECRYPT_MODE);
        // Assert.assertSame(cipher, defaultCipherFactory.decryptionCipher());
        Assert.assertEquals(cipher, defaultCipherFactory.decryptionCipher());
    }

    // @Test(expected = XlpRuntimeException.class)
    // public void testInitCipherWithXlpRuntimeException() throws Exception {
    //     Mockito.doThrow(new NoSuchPaddingException()).when(defaultCipherFactory).obtainCipher(Cipher.ENCRYPT_MODE);
    //     defaultCipherFactory.initCipher(Cipher.ENCRYPT_MODE);
    // }

    @Test
    public void testInitCipher() throws Exception {
        // Mockito.doReturn(cipher).when(defaultCipherFactory).obtainCipher(Cipher.ENCRYPT_MODE);
        Assert.assertEquals(cipher, defaultCipherFactory.initCipher(1));
    }

    @Test
    public void testObtainCipher() throws Exception {
        // Assert.assertNotNull(defaultCipherFactory.obtainCipher(Cipher.ENCRYPT_MODE));
	assert defaultCipherFactory.obtainCipher(1) != null;
    }

    @Test
    public void testKey() {
        Assert.assertArrayEquals(keyString.getBytes(), defaultCipherFactory.key());
    }

    // @Test
    // public void testKeyBase64() {
    //     // defaultCipherFactory.setKey(Base64.encodeBase64String(keyString.getBytes()));
    //     defaultCipherFactory.setKey(new String(keyString.getBytes()));
    //     defaultCipherFactory.setKeyBase64(true);
    //     Assert.assertArrayEquals(keyString.getBytes(), defaultCipherFactory.key());
    // }
}

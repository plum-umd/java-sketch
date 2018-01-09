public class CipherFactoryTests {
    harness public void main() {
	// DefaultCipherFactoryTest cft = new DefaultCipherFactoryTest();
	// cft.setUp();
	// cft.testEncryptionCipher();

	CryptoManager cm = new CryptoManager();

	String m = "Secret message";

	String d = cm.encrypt(m);

	String p = cm.decrypt(d);

	assert p.equals(m);	
    }
}

public class Tester {
    harness public void main() {
	testOpenSSL();
	testJCECipher();
    }

    public void testOpenSSL() {
	OpenSSLCipher oc = new OpenSSLCipher("AES", "TRANSFORMATION");
	byte[] plaintext = new byte[32];
	byte[] IV = new byte[8];
	byte[] key = new byte[128];
	
	for (int i = 0; i < 128; i ++) {
	    key[i] = i;
	    if (i < 32) plaintext[i] = i;
	    if (i < 8) IV[i] = i;
	}

	Key sk = new SecretKeySpec(key, "AES");

	byte[] cipherText = oc.encrypt(plaintext, sk, IV);

	byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);
	
	assert Arrays.arraysEquals(plaintext, plaintext2);
    }

    public void testJCECipher() {
	JCECipher oc = new JCECipher("PROVIDER", "AES", "TRANSFORMATION");
	byte[] plaintext = new byte[32];
	byte[] IV = new byte[8];
	byte[] key = new byte[128];
	
	for (int i = 0; i < 128; i ++) {
	    key[i] = i;
	    if (i < 32) plaintext[i] = i;
	    if (i < 8) IV[i] = i;
	}

	Key sk = new SecretKeySpec(key, "AES");

	byte[] cipherText = oc.encrypt(plaintext, sk, IV);

	byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);
	
	assert Arrays.arraysEquals(plaintext, plaintext2);
    }
}

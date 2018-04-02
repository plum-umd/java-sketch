public class Tester {
    // harness public void main(int x, int y, int z) {
    // 	assume x != y != z;
    // 	assume x > 0 && x < 9999999;
    // 	assume y > 0 && y < 9999999;
    // 	assume z > 0 && z < 9999999;
    // 	testOpenSSL(x, y, z);
    // 	testJCECipher(x, y, z);
    // }

    harness public void main() {
	testOpenSSL();
	testJCECipher();
    }
    
    public void testOpenSSL() {
	OpenSSLCipher oc = new OpenSSLCipher("AES", "TRANSFORMATION");

	for (int x = 0; x < 999999; x = x + 111111) {	
	    String p1 = Integer.toString(x);
	    String p2 = Integer.toString(x+1);
	    String p3 = Integer.toString(x+2);

	    byte[] plaintext = p1.getBytes();
	    byte[] IV = p2.getBytes();
	    byte[] key = p3.getBytes();

	    Key sk = new SecretKeySpec(key, "AES");
	    byte[] cipherText = oc.encrypt(plaintext, sk, IV);
	    byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);	
	    assert Arrays.arraysEquals(plaintext, plaintext2);
	}
    }

    public void testJCECipher() {
	JCECipher oc = new JCECipher("PROVIDER", "AES", "TRANSFORMATION");


	for (int x = 0; x < 999999; x = x + 111111) {
	    String p1 = Integer.toString(x);
	    String p2 = Integer.toString(x+1);
	    String p3 = Integer.toString(x+2);

	    byte[] plaintext = p1.getBytes();
	    byte[] IV = p2.getBytes();
	    byte[] key = p3.getBytes();

	    Key sk = new SecretKeySpec(key, "AES");
	    byte[] cipherText = oc.encrypt(plaintext, sk, IV);
	    byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);

	    assert Arrays.arraysEquals(plaintext, plaintext2);
	}
    }

    // public void testOpenSSL(int x, int y, int z) {
    // 	OpenSSLCipher oc = new OpenSSLCipher("AES", "TRANSFORMATION");

    // 	String p1 = Integer.toString(x);
    // 	String p2 = Integer.toString(y);
    // 	String p3 = Integer.toString(z);

    // 	byte[] plaintext = p1.getBytes();
    // 	byte[] IV = p2.getBytes();
    // 	byte[] key = p3.getBytes();
	
    // 	// byte[] plaintext = new byte[32];
    // 	// byte[] IV = new byte[8];
    // 	// byte[] key = new byte[128];
	
    // 	// for (int i = 0; i < 128; i ++) {
    // 	//     key[i] = i;
    // 	//     if (i < 32) plaintext[i] = i;
    // 	//     if (i < 8) IV[i] = i;
    // 	// }

    // 	Key sk = new SecretKeySpec(key, "AES");

    // 	byte[] cipherText = oc.encrypt(plaintext, sk, IV);

    // 	byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);
	
    // 	assert Arrays.arraysEquals(plaintext, plaintext2);
    // }

    // public void testJCECipher(int x, int y, int z) {
    // 	JCECipher oc = new JCECipher("PROVIDER", "AES", "TRANSFORMATION");

    // 	String p1 = Integer.toString(x);
    // 	String p2 = Integer.toString(y);
    // 	String p3 = Integer.toString(z);

    // 	byte[] plaintext = p1.getBytes();
    // 	byte[] IV = p2.getBytes();
    // 	byte[] key = p3.getBytes();

    // 	// byte[] plaintext = new byte[32];
    // 	// byte[] IV = new byte[8];
    // 	// byte[] key = new byte[128];
	
    // 	// for (int i = 0; i < 8; i ++) {
    // 	//     key[i] = i;
    // 	//     if (i < 8) plaintext[i] = i;
    // 	//     if (i < 8) IV[i] = i;
    // 	// }

    // 	Key sk = new SecretKeySpec(key, "AES");

    // 	byte[] cipherText = oc.encrypt(plaintext, sk, IV);

    // 	byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);
	
    // 	assert Arrays.arraysEquals(plaintext, plaintext2);
    // }
}

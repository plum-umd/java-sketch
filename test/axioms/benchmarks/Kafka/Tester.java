public class Tester {
    harness public void main() {
	testOpenSSL();
	testJCECipher();
    }
    
    public void testOpenSSL() {
	OpenSSLCipher oc = new OpenSSLCipher("AES", "TRANSFORMATION");

	// for (int x = 0; x < 666666; x = x + 111111) {	
	// for (int x = 9; x < 5000000; x = x * 9) {
	for (int x = 0; x < 5; x++) {		    	    
	// for (int x = 666666; x < 666667; x = x + 111111) { 
	    String p1 = Integer.toString(x);
	    String p2 = Integer.toString(x+1);
	    String p3 = Integer.toString(x+2);

	    byte[] plaintext = p1.getBytes();
	    byte[] IV = p2.getBytes();
	    byte[] key = p3.getBytes();

	    // Key sk = new SecretKeySpec(key, "AES");
	    SecretKeySpec sk = new SecretKeySpec();
	    byte[] cipherText = oc.encrypt(plaintext, sk, IV);
	    byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);	
	    assert Arrays.arraysEquals(plaintext, plaintext2);
	}
    }

    public void testJCECipher() {
    	JCECipher oc = new JCECipher("PROVIDER", "AES", "TRANSFORMATION");

    	// for (int x = 0; x < 666666; x = x + 111111) {
    	// for (int x = 9; x < 5000000; x = x * 9) {		    
    	for (int x = 0; x < 5; x++) {		    
    	// for (int x = 666666; x < 666667; x = x + 111111) {	
    	    String p1 = Integer.toString(x);
    	    String p2 = Integer.toString(x+1);
    	    String p3 = Integer.toString(x+2);

    	    byte[] plaintext = p1.getBytes();
    	    byte[] IV = p2.getBytes();
    	    byte[] key = p3.getBytes();

    	    // Key sk = new SecretKeySpec(key, "AES");
    	    SecretKeySpec sk = new SecretKeySpec();
    	    byte[] cipherText = oc.encrypt(plaintext, sk, IV);
    	    byte[] plaintext2 = oc.decrypt(cipherText, sk, IV);

    	    assert Arrays.arraysEquals(plaintext, plaintext2);
    	}
    }

}

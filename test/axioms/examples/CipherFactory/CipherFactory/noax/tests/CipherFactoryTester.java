public class CipherFactoryTests {
    // harness public void main(int x) {
    // 	assume x > 0 && x < 999999;
    // 	// DefaultCipherFactoryTest cft = new DefaultCipherFactoryTest();
    // 	// cft.setUp();
    // 	// cft.testEncryptionCipher();

    // 	CryptoManager cm = new CryptoManager();

    // 	// String m = "Secret message";
    // 	String m = Integer.toString(x);
	
    // 	String d = cm.encrypt(m);
    // 	assert !d.equals(m);
    // 	String p = cm.decrypt(d);

    // 	assert p.equals(m);	
    // }

    harness public void main() {
    	// DefaultCipherFactoryTest cft = new DefaultCipherFactoryTest();
    	// cft.setUp();
    	// cft.testEncryptionCipher();

    	// int x = 1;
	
    	CryptoManager cm = new CryptoManager();


    	for (int x = 9; x < 5000000; x = x * 9) {	
    	// for (int x = 0; x < 999999; x = x + 111111) {
    	// for (int x = 0; x < 5; x = x + 1) {	    
    	    // String m = "Secret message";
    	    String m = Integer.toString(x);	
    	    String d = cm.encrypt(m);
    	    assert !m.equals(d);
    	    String p = cm.decrypt(d);
    	    assert p.equals(m);	
    	}
	    
    	// m = Integer.toString(99);	
    	// d = cm.encrypt(m);
    	// p = cm.decrypt(d);
    	// assert p.equals(m);	

    	// m = Integer.toString(1234);	
    	// d = cm.encrypt(m);
    	// p = cm.decrypt(d);
    	// assert p.equals(m);	
    }

    // harness public void main() {
    // 	// DefaultCipherFactoryTest cft = new DefaultCipherFactoryTest();
    // 	// cft.setUp();
    // 	// cft.testEncryptionCipher();

    // 	CryptoManager cm = new CryptoManager();

    // 	String m = "Secret message";

    // 	String d = cm.encrypt(m);

    // 	String p = cm.decrypt(d);

    // 	assert p.equals(m);	
    // }
}

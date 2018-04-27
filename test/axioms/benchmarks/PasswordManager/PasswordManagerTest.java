public class PasswordManagerTest {

    // PasswordManager pasman;
    
    // harness public void main(/*String[] args*/) throws InvalidKeyException,
    // 			IllegalBlockSizeException, BadPaddingException,
    // 			NoSuchAlgorithmException, NoSuchPaddingException,
    // 			NoSuchProviderException, IOException,
    // 			InvalidParameterSpecException, InvalidAlgorithmParameterException,
    // 			DecoderException, ClassNotFoundException {
    // 		pasman = new PasswordManager("1234");
    // 		testAddGet();

    // 		//pasman.modifyPassword("google", "5115");		
    // 		// try{
			
    // 		// 	String s = pasman.getPass("google");
    // 		// 	System.out.println("Password for google.com is : "+s);
    // 		// }catch (NullPointerException e) {
    // 		// 	System.err.println("Password not found");
    // 		// }

    // 	}

    // harness public static void main() {
    // 	// int limit = 9999999;
    // 	// int limit = 100;
    // 	// assume u > 0 & u < limit;
    // 	// assume w > 0 & w < limit;
    // 	// assume x > 0 & x < limit;
    // 	// assume y > 0 & y < limit;
    // 	// assume z > 0 & z < limit;	
    // 	// assume u != w && w != y && x != z;

    // 	String p1 = Integer.toString(12345);
	
    // 	PasswordManager pasman = new PasswordManager(p1);	
	
    // 	for (int i = 1; i < 5; i++) {
    // 	    String p2 = Integer.toString(i*81);
    // 	    String p3 = Integer.toString(i*891);
    // 	    String p4 = Integer.toString(i*8019);
    // 	    String p5 = Integer.toString(i*72171);	
	    
    // 	    pasman.addPassword(p2, p3);
    // 	    pasman.addPassword(p4, p5);
    // 	    String pass1 = pasman.getPass(p2);	
    // 	    assert pass1.equals(p3);	
    // 	    String pass2 = pasman.getPass(p4);	
    // 	    assert pass2.equals(p5);
    // 	    pasman.modifyPassword(p2, p4);
    // 	    String pass3 = pasman.getPass(p2);	
    // 	    assert pass3.equals(p4);	
    // 	}
		
    // 	// assert !pasman.checkMasterPassword(p2);
    // 	// assert pasman.checkMasterPassword(p1);

    // }

    harness public static void main(int u, int w, int x, int y, int z) {
    	// int limit = 9999999;
    	int limit = 100;
    	assume u > 0 & u < limit;
    	assume w > 0 & w < limit;
    	assume x > 0 & x < limit;
    	assume y > 0 & y < limit;
    	assume z > 0 & z < limit;	
    	assume u != w && w != y && x != z;
	
    	String p1 = Integer.toString(u);
    	String p2 = Integer.toString(w);
    	String p3 = Integer.toString(x);
    	String p4 = Integer.toString(y);
    	String p5 = Integer.toString(z);

    	PasswordManager pasman = new PasswordManager(p1);

    	pasman.addPassword(p2, p3);
    	pasman.addPassword(p4, p5);
    	String pass1 = pasman.getPass(p2);	
    	assert pass1.equals(p3);	
    	String pass2 = pasman.getPass(p4);	
    	assert pass2.equals(p5);
    	pasman.modifyPassword(p2, p4);
    	String pass3 = pasman.getPass(p2);	
    	assert pass3.equals(p4);	
	
    	// assert !pasman.checkMasterPassword(p2);
    	// assert pasman.checkMasterPassword(p1);

    }
    
    // harness public static void main() {	
    // 	PasswordManager pasman = new PasswordManager("1234");
	
    // 	pasman.addPassword("yahoo", "12345");
    // 	pasman.addPassword("google", "5441944");
    // 	String pass1 = pasman.getPass("google");

    // 	assert pass1.equals("5441944");

    // 	String pass2 = pasman.getPass("yahoo");

    // 	assert pass2.equals("12345");

    // 	assert !pasman.checkMasterPassword("12345");
    // 	assert pasman.checkMasterPassword("1234");
    // 	// testAddGet();

    // 	//pasman.modifyPassword("google", "5115");		
    // 	// try{

    // 	// 	String s = pasman.getPass("google");
    // 	// 	System.out.println("Password for google.com is : "+s);
    // 	// }catch (NullPointerException e) {
    // 	// 	System.err.println("Password not found");
    // 	// }

    // }
    
    
    // public void testAddGet() {
    // 	pasman.addPassword("yahoo", "12345");
    // 	pasman.addPassword("google", "5441944");
    // 	String pass1 = pasman.getPass("google");

    // 	// assert pass1.equals("12345");
    // }
}

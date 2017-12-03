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

    harness public static void main(// String[] args
				    ) {
		PasswordManager pasman = new PasswordManager("1234");

		pasman.addPassword("yahoo", "12345");
		pasman.addPassword("google", "5441944");
		String pass1 = pasman.getPass("google");
		
		// testAddGet();

		//pasman.modifyPassword("google", "5115");		
		// try{
			
		// 	String s = pasman.getPass("google");
		// 	System.out.println("Password for google.com is : "+s);
		// }catch (NullPointerException e) {
		// 	System.err.println("Password not found");
		// }

    }
    
    
    // public void testAddGet() {
    // 	pasman.addPassword("yahoo", "12345");
    // 	pasman.addPassword("google", "5441944");
    // 	String pass1 = pasman.getPass("google");

    // 	// assert pass1.equals("12345");
    // }
}

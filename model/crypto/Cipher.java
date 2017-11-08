public class Cipher {

    private String mode;
    
    public Cipher(String mode) {
	this.mode = mode;
    }

    public static Cipher getInstance(String mode) {
	return new Cipher(mode);
    }

    public void init(int opmode, Certificate certificate) {
	
    }

    public byte[] doFinal(byte[] text) {
	return text;
    }
    
}

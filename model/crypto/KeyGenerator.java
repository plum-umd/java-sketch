
public class KeyGenerator {

    private String mode;
    
    public KeyGenerator(String mode) {
	this.mode = mode;
    }

    public Key generateKey() {
	return new KerberosKey();
    }

    public void init(int keysize) {

    }

    public static KeyGenerator getInstance(String mode) {
    	return new KeyGenerator(mode);
    }
    
}

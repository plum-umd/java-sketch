public class CryptoCipherFactory {
    public String CLASSES_KEY;

    public CryptoCipherFactory() {
	CLASSES_KEY = "CLASSES_KEY";
    }

    public class CipherProvider {
	public CipherProvider() {

	}

	public static String getClassName() {
	    return "OPENSSL";
	}
    }
    
}

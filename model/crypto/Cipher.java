public class Cipher {

    private String type;
    private Key key;
    private int mode;
    
    public int ENCRYPT_MODE;
    public int DECRYPT_MODE;
    
    public Cipher(String type) {
	this.type = type;
	this.ENCRYPT_MODE = 1;
	this.DECRYPT_MODE = 2;
    }

    public static Cipher getInstance(String type) {
    	return new Cipher(type);
    }

    public static Cipher getInstance(String type, String extra) {
	return new Cipher(type);
    }

    public void init(int opmode, Key key) {
	this.key = key;
	this.mode = opmode;
    }

    public void init(int opmode, SecretKey key, IvParameterSpec i) {
    	this.key = key;
    	this.mode = opmode;
    }

    // Commented for PasswordManager Example
    // public void init(int opmode, SecretKey key, AlgorithmParameterSpec i) {
    // 	this.key = key;
    // 	this.mode = opmode;
    // }
    
    public byte[] doFinal(byte[] text) {
	byte[] k = key.getEncoded();
	byte[] result = new byte[text.length];
	if (k.length == 0) {
	    return result;
	}
	if (mode == ENCRYPT_MODE) {
	    for (int i = 0; i < text.length; i++) {
		result[i] = text[i] + k[i%k.length];
	    }
	} else if (mode == DECRYPT_MODE) {
	    for (int i = 0; i < text.length; i++) {
		result[i] = text[i] - k[i%k.length];
	    }
	}
	return result;
    }

    public int getOutputSize(int length) {
	return length;
    }

    public int update(byte[] data, int i, int l, byte[] out, int j) {
	return 0;
    }

    public int doFinal(byte[] data, int i, int l, byte[] out, int j) {
	out = doFinal(data);
	return data.length;
    }
    
}

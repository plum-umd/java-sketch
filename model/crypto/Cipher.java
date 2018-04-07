public class Cipher {

    private String type;
    private Key key;
    private int mode;
    private boolean[] updated;
    
    public int ENCRYPT_MODE;
    public int DECRYPT_MODE;
    
    public Cipher(String type) {
	this.type = type;
	this.ENCRYPT_MODE = 1;
	this.DECRYPT_MODE = 2;
	this.updated = null;
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
    public void init(int opmode, SecretKey key, AlgorithmParameterSpec i) {
    	this.key = key;
    	this.mode = opmode;
    }
    
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
	return length+1;
    }

    public int update(byte[] data, int i, int l, byte[] out, int j) {
	if (updated == null) {
	    updated = new boolean[getOutputSize(data.length)];
	}	
	for (int k = i; k < l; k++) {
	    updated[k] = true;
	}
	return l-i;
    }

    public int doFinal(byte[] text, int i, int l, byte[] out, int j) {
	byte[] k = key.getEncoded();
	// byte[] result = new byte[text.length];
	int crypted = 0;
	if (k.length == 0) {
	    return 0;
	}
	if (mode == ENCRYPT_MODE) {
	    for (int w = 0; w < text.length; w++) {
	    	if (updated[w] || (w >= i && w < l)) {
		    if (!(updated[w])) {
			crypted ++;
		    }
	    	    out[w] = text[w] + k[w%k.length];
	    	}
	    }
	} else if (mode == DECRYPT_MODE) {
	    for (int w = 0; w < text.length; w++) {
	    	if (updated[w] || (w >= i && w < l)) {
		    if (!(updated[w])) {
			crypted ++;
		    }
	    	    out[w] = text[w] - k[w%k.length];
	    	}
	    }
	}
	return crypted;
    }
    
}

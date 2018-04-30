public class SecretKeySpec implements Key{

    private byte[] key;

    public SecretKeySpec(byte[] key, String type) {
	this.key = key;
    }

    public byte[] getEncoded() {
	return this.key;
    }
    
    
}

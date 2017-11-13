
public class KerberosKey implements Key {

    private byte[] key;
    private int KEYSIZE;
    
    public KerberosKey() {
	KEYSIZE = 32;
	key = new byte[KEYSIZE];
	for(int i=0; i < KEYSIZE; i++) {
	    key[i] = 1;
	}	
    }

    public byte[] getEncoded() {
	return key;
    }
}

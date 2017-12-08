public class SecureRandom {
    public SecureRandom() {

    }

    public void nextBytes(byte[] buf) {
	for (int i = 0; i < buf.length; i++) {
	    buf[i] = (byte) i;
	}
    }
}

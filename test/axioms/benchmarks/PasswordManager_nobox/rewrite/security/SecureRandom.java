@rewriteClass
public class SecureRandom {
    @alg
    @pure
    // byte[] nextBytes(Object k);
    byte[] nextBytes(byte[] k);

    // rewrite Object nextBytes(SecureRandom s, Object k) {
    rewrite Object nextBytes(Object SecureRandom(), byte[] k) {
    	return new byte[16];
    }
}

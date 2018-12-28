@rewriteClass
public class SecureRandom {
    @alg
    @constructor
    SecureRandom SecureRandom(Bytes bs);

    @alg
    @pure
    // byte[] nextBytes(Object k);
    byte[] nextBytes(byte[] k);

    // // rewrite Object nextBytes(SecureRandom s, Object k) {
    // rewrite Object nextBytes(Object SecureRandom(), byte[] k) {
    // 	return new byte[16];
    // }

    rewrite Object nextBytes(Object SecureRandom(Bytes bs), byte[] k) {
	return new byte[16];
    }
}

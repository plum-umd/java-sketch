@rewriteClass
public class SecureRandom {
    @alg
    @pure
    void nextBytes(Object k);

    rewrite Object nextBytes(SecureRandom s, Object k) {
	return new byte[16];
    }
}

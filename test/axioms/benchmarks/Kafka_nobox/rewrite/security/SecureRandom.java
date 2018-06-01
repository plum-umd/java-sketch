@rewriteClass
public class SecureRandom {
    @alg
    @pure
    byte[] nextBytes(Object k);

    rewrite Object nextBytes(SecureRandom s, Object k) {
	return new byte[16];
    }
}

// @rewriteClass
// public class SecureRandom {
//     @alg
//     @pure
//     void nextBytes(Object k);

//     rewrite Object nextBytes(SecureRandom s, Object k) {
// 	return new byte[16];
//     }
// }

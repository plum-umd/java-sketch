@rewriteClass
public class SecretKeySpec implements Key {
    @alg
    @pure
    byte[] getEncoded();

    // @alg
    // @constructor
    // SecretKeySpec SecretKeySpec(byte[] k, String alg);

    @alg
    @pure
    // boolean equals(Object o);
    boolean equals(SecretKeySpec s);

    // rewrite Object equals(SecretKeySpec s, Object SecretKeySpec()) {
    rewrite Object equals(SecretKeySpec s1, SecretKeySpec s2) {
    	return true;
    }
}

// public class SecretKeySpec implements Key {
//     // @alg
//     // @pure
//     // byte[] getEncoded();

//     // @alg
//     // @constructor
//     // SecretKeySpec SecretKeySpec(byte[] k, String alg);

//     byte[] k;
//     String alg;
    
//     public SecretKeySpec(byte[] k, String alg) {
// 	this.k = k;
// 	this.alg = alg;
//     }
    
//     public byte[] getEncoded() {
// 	return k;
//     }

//     public boolean equals(Object o) {
// 	if (o instanceof SecretKeySpec) {
	    
// 	}
//     }
// }

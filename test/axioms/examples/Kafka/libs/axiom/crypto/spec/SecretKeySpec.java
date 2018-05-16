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
    boolean equals(Object o);

    rewrite Object equals(SecretKeySpec s, Object SecretKeySpec()) {
    	return true;
    }
}

// public class SecretKeySpec implements Key {
//     // @adt
//     // @pure
//     // byte[] getEncoded();

//     // @adt
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

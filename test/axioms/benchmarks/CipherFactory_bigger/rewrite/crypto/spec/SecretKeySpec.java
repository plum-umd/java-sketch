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
    // boolean equals(SecretKeySpec s);
    boolean equals(Object s);

    // rewrite Object equals(SecretKeySpec s, Object SecretKeySpec()) {
    // rewrite Object equals(SecretKeySpec s1, SecretKeySpec s2) {
    rewrite Object equals(Object SecretKeySpec(), Object s2) {
    	return true;
    }

    rewrite Object getEncoded(Object SecretKeySpec()) {
    	return new byte[16];
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

@axiomClass
public class SecretKeySpec implements Key {
    @adt
    @pure
    byte[] getEncoded();

    // @adt
    // @constructor
    // SecretKeySpec SecretKeySpec(byte[] k, String alg);

    @adt
    @pure
    boolean equals(Object o);

    axiom Object equals(SecretKeySpec s, Object SecretKeySpec()) {
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

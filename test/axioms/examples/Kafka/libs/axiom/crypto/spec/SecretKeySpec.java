@axiomClass
// public class SecretKeySpec implements Key {
public class SecretKeySpec {
    @adt
    @pure
    byte[] getEncoded();
    
    @adt
    @constructor
    SecretKeySpec SecretKeySpec(byte[] k, String alg);
}

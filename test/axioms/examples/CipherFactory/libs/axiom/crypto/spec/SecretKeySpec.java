@axiomClass
public class SecretKeySpec implements Key {
    @adt
    @pure
    byte[] getEncoded();

    @adt
    @constructor
    SecretKeySpec SecretKeySpec(byte[] k, String alg);
}

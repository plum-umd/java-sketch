@axiomClass
public class SecureRandom {
    @adt
    @pure
    void nextBytes(byte k);

    axiom Object nextBytes(SecureRandom s, byte k) {
	return new byte[16];
    }
}

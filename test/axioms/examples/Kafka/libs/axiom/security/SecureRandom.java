@axiomClass
public class SecureRandom {
    @adt
    @pure
    void nextBytes(Object k);

    axiom Object nextBytes(SecureRandom s, Object k) {
	return new byte[16];
    }
}

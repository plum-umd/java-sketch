@axiomClass
public class Mac {
    @adt
    void init(SecretKeySpec key);

    @adt
    @pure
    byte[] doFinal(byte text);

    axiom Object doFinal(Object init!(Mac m, SecretKeySpec s), byte text) {
	return text;
    }
}

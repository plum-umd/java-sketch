@axiomClass
public class Mac {
    @adt
    void init(SecretKeySpec key);

    @adt
    @pure
    Object doFinal(Object text);

    axiom Object doFinal(Object init!(Mac m, SecretKeySpec s), Object text) {
	return text;
    }
}

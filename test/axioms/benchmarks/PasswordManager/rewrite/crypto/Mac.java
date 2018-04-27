@rewriteClass
public class Mac {
    @alg
    void init(SecretKeySpec key);

    @alg
    @pure
    Object doFinal(Object text);

    rewrite Object doFinal(Object init!(Mac m, SecretKeySpec s), Object text) {
	return text;
    }
}

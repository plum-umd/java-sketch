@rewriteClass
@autoBox
class Cipher {

    public static Cipher getInstance(String type) {
    	return new Cipher(type);
    }

    @alg
    @pure
    String toString(Object txt);
    
    @alg
    @constructor
    Cipher Cipher(String t);

    // @alg
    // void getInstance(String type);
    
    @alg
    void init(int mode, Object k, Object iv);
    
    @alg
    Object doFinal(Object text);
    
    // rewrite Object doFinal(Object init!(Cipher c1, int m1, Object k1, Object iv1), Object toString(Cipher c3, Object doFinal!(Object init!(Cipher c2, int m2, Object k2, Object iv2), Object t))) {
    // 	return k1.equals(k2) ? ((m1 == 2 && m2 == 1) ? t : null) : null;
    // }

    rewrite Object doFinal(Object init!(Cipher c1, int m1, Object k1, Object iv1), Object doFinal(Object init!(Cipher c2, int m2, Object k2, Object iv2), Object t)) {
    	return k1.equals(k2) ? ((m1 == 2 && m2 == 1) ? t : null) : null;
    }
    
    // rewrite Object doFinal(Object init!(Object getInstance!(Cipher c1, String type1), int m1, Object k1), Object doFinal(Object init!(Cipher c2, int m2, Object k2), Object t)) {
    // 	return k1.equals(k2) ? t : null;
    // }
    
}

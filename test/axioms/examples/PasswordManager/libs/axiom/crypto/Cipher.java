@axiomClass
class Cipher {

    public static Cipher getInstance(String type) {
    	return new Cipher(type);
    }

    @adt
    @pure
    String toString();
    
    @adt
    @constructor
    Cipher Cipher(String t);

    // @adt
    // void getInstance(String type);
    
    @adt
    void init(int mode, Object k, Object iv);
    
    @adt
    Object doFinal(Object text);
    
    axiom Object doFinal(Object init!(Cipher c1, int m1, Object k1, Object iv1), Object toString(Object doFinal!(Object init!(Cipher c2, int m2, Object k2, Object iv2), Object t))) {
    	return k1.equals(k2) ? ((m1 == 2 && m2 == 1) ? t : null) : null;
    }

    // axiom Object doFinal(Object init!(Object getInstance!(Cipher c1, String type1), int m1, Object k1), Object doFinal(Object init!(Cipher c2, int m2, Object k2), Object t)) {
    // 	return k1.equals(k2) ? t : null;
    // }
    
}

@axiomClass
class Cipher {

    public static Cipher getInstance(String type) {
    	return new Cipher(type);
    }

    // @adt
    // void getInstance(String type);
    
    @adt
    void init(int mode, Object k);
    
    @adt
    byte[] doFinal(byte[] text);
    
    axiom Object doFinal(Object init!(Cipher c1, int m1, Object k1), Object doFinal(Object init!(Cipher c2, int m2, Object k2), byte[] t)) {
    	return k1.equals(k2) ? t : null;
    }

    // axiom Object doFinal(Object init!(Object getInstance!(Cipher c1, String type1), int m1, Object k1), Object doFinal(Object init!(Cipher c2, int m2, Object k2), Object t)) {
    // 	return k1.equals(k2) ? t : null;
    // }
    
}

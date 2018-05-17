@axiomClass
class Cipher {

    public static Cipher getInstance(String type) {
    	return new Cipher(type);
    }

    @adt
    @constructor
    Cipher Cipher(String type);
    
    @adt
    void init(int mode, Object k, Object iv);

    @adt
    byte[] doFinal(byte[] text);
    
    axiom byte[] doFinal(Object init!(Cipher c1, int m1, Object k1, Object iv1), byte[] doFinal(Object init!(Cipher c2, int m2, Object k2, Object iv2), byte[] t)) {
    	return k1.equals(k2) ? ((m1 == 2 && m2 == 1) ? t : null) : null;
    }

    axiom byte[] doFinal(Object Cipher(), byte[] t) {
    	return t;
    }

    axiom byte[] doFinal(Object Cipher(String type), byte[] t) {
    	return type;
    }    
}

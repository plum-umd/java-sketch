@axiomClass
class Cipher {

    @adt
    void init(int mode, Object k);
    
    @adt
    Object doFinal(Object text);
    
    axiom Object doFinal(Object init!(Cipher c1, int m1, Object k1), Object doFinal(Object init!(Cipher c2, int m2, Object k2), Object t)) {
    	return k1.equals(k2) ? t : null;
    }

}

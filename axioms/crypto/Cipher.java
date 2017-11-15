@axiomClass
class Cipher {

    @adt
    void init(Object mode, Object k);
    
    @adt
    Object doFinal(Object text);
    
    // axiom Object doFinal(Object init!(Cipher c, Object m2, Object k2), Object t2) {
    // 	return 0;
    // }

    axiom Object doFinal(Object init!(Cipher c1, Object m2, Object k2), Object doFinal!(Object init!(Cipher c2, Object m1, Object k1), Object t)) {
    	return 0;
    }

}

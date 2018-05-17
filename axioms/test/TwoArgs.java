@axiomClass
public class TwoArgs {

    @adt
    void init(Object e);
    
    @adt
    int decrypt(Object e1, Object e2);

    @adt
    int encrypt(Object e);

    axiom Object decrypt(Object init!(Object init!(TwoArgs t1, Object e1), Object e3), Object t3, Object encrypt!(Object init!(TwoArgs t2, Object e2))) {
	return 0;
    }
}

@axiomClass
public class Generics<A, B> {
    @adt
    A get1(A e1, B e2, int i, Object o);

    @adt
    B get2();

    axiom Object get1(Object get2!(Generics g), A a, B b, int i1, Object o1) {
	return i > 0 ? a : b;
    }
}

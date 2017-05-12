class DifferentTypeVars<T> {
    harness void mn() {
    }
    void f(T t) {
	M<T> m = new M<T>(t);
    }
}
class M<E> {
    M(E e) { }
}

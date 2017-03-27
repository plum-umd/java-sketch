class Outer {
    class Inner {
	int x;
	Inner i;
	Outer o2;
	Inner()  { this.x = 2; }
	Inner(int x)  { this.x = x; }
	void m() { a = 5; }
    }
    void m(Inner i1) { i1.x = 1; }
    int a;
    Outer o1;
    Inner i;
    Outer() { i = new Inner(); }
    Outer(int x) { i = new Inner(x); }
}
class NestedCls {
    void main(int x) {
    // harness void main(int x) {
	Outer o1 = new Outer();
	assert o1.i.x == 2;
	o1.m(o1.i);
	assert o1.i.x == 1;
	o1.i.m();
	assert o1.a == 5;

	Outer o2 = new Outer(x);
	assert o2.i.x == x;
    }
}

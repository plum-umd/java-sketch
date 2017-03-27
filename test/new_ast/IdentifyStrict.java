class A { }
class B extends A { }
interface I { }
class C implements I { }
class D extends C { }
class IdentifyStrict {
    void m(byte a) { } 
    void m(char a) { } 
    void m(short a) { } 
    void m(int a) { } 
    void m(long a) { } 
    void m(float a) { } 
    void m(double a) { } 
    void m(A a) { } 
    void m(B b) { } 
    void m(I i) { } 
    void m(C c) { } 
    harness void main() {
	byte b = 0;
	m(b); // m_byte
	char c = 0;
	m(c); // m_char
	short s = 0;
	m(s); // m_short
	int i = 0;
	m(i); // m_int
	long l = 0.0;
	m(l); // m_long
	float f = 0.0;
	m(f); // m_float
	double d = 0.0;
	m(d); // m_double

	A ca = new A();
	m(ca); // m_A

	B cb = new B();
	m(cb); // m_B

	I ic = new C();
	m(ic); // m_I

	I id = new D();
	m(id); // m_I

	C cc = new C();
	m(cc); // m_C
    }
}

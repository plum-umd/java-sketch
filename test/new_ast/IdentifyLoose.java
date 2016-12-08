class UnBox {
    void m(Byte a) { } 
    void m(Char a) { } 
    void m(Integer a) { } 
    void m(Long a) { } 
    void m(Float a) { } 
    void m(Double a) { } 
    void test() {
	byte b = 0;
	m(b); // m_Byte
	char c = 0; 
	m(c); // m_Char
	int i1;
	m(i1); // m_Integer
	long l = 0;
	m(l); // m_Long
	float f = 0;
	m(f); // m_Float
	double d = 0.0;
	m(d); // m_Double
    }
}

class Box {
    void m(byte a) { } 
    void m(char a) { } 
    void m(int a) { } 
    void m(long a) { } 
    void m(float a) { } 
    void m(double a) { } 
    void test() {
	Byte b = 0;
	m(b); // m_byte
	Char c = 0; 
	m(c); // m_char
	Integer i = 0;
	m(i); // m_int
	Long l = 0;
	m(l); // m_long
	Float f = 0;
	m(f); // m_float
	Double d = 0.0;
	m(d); // m_double
    }
}

class IdentifyLoose {
    void m(byte a) { } 
    void m(char a) { } 
    void m(long a) { } 
    void m(float a) { } 
    void m(double a) { } 
    harness void main() {
	// TODO: going to require type cast
	// int i = 0;
	// m(i); // m_long
    }
}

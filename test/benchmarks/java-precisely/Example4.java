// Example 4 from page 7 of Java Precisely third edition (The MIT Press 2016)
// Author: Peter Sestoft (sestoft@itu.dk)


class Example4 {
  public static void main(String[] args) {
    int i1 = 1000111222, i2 = 40000, i3 = -1;
    floatdouble((float)i1, (double)i1);                           // L W: 1.00011123E9 1.000111222E9
    bytecharshort1((byte)i2, (char)i2, (short)i2);  // C C C: 64 40000 -25536
    bytecharshort2((byte)i3, (char)i3, (short)i3);  // C C C: -1 65535 -1
    intint1((int)1.9, -(int)1.9);                   // C C: 1 -1
    intint2((int)1.5, -(int)1.5);                   // C C: 1 -1
    intint3((int)2.5, -(int)2.5);                   // C C: 2 -2
  }

  private static void floatdouble(float f, double d) { 
    assert f == 1.00011123E9;
    assert d == 1.000111222E9;
  }

  private static void bytecharshort1(byte b, char c, short s) { 
    assert b == 64;
    assert (int)c == 40000;
    assert s == -25536;
  }

  private static void bytecharshort2(byte b, char c, short s) { 
    assert b == -1;
    assert (int)c == 65535;
    assert s == -1;
  }

  private static void intint1(int i1, int i2) { 
    assert i1 == 1;
    assert i2 == -1;
  }

  private static void intint2(int i1, int i2) { 
    assert i1 == 1;
    assert i2 == -1;
  }

  private static void intint3(int i1, int i2) { 
    assert i1 == 2;
    assert i2 == -2;
  }
}


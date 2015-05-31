package java.lang;

public class String implements CharSequence {
  char[] _value;
  int _count;

  // use this constructor as it includes "count"
  // ignore offset at the moment
  public String(char[] ca, int offset, int count) {
    _value = ca;
    _count = count;
  }

  public char charAt(int index) {
    if (0 <= index && index < _count) return _value[index];
  }

  public int length() {
    return _count;
  }

  public String toString() {
    return this;
  }

  public boolean equals(String s) {
    return _value == s._value;
  }
}

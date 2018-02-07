package java.lang;

public class StringBuilder implements CharSequence {
  char[] _value;
  int _count;
    
  public StringBuilder() {
      _value = new char[1];
      _count = 0;
  }
    
  public StringBuilder(String str) {
    _value = str._value;
    _count = str.length();
  }

  public char charAt(int index) {
    if (0 <= index && index < _count) return _value[index];
  }

  public int length() {
    return _count;
  }

  public String toString() {
    return new String(_value, 0, _count);
  }

  public void setCharAt(int i, char c) {
    _value[i] = c;
  }

  public void append(String s) {
      int len = s.length();
      int new_value_len = _count+len;
      char[] new_value = new char[new_value_len];

      for (int i = 0; i < _count; i++) {
	  new_value[i] = _value[i];
      }

      for (int i = 0; i < len; i++) {
	  new_value[_count+i] = s.charAt(i);
      }

      _value = new_value;
      _count = new_value_len;
  }

  public void append(char c) {
      int new_value_len = _count+1;
      char[] new_value = new char[new_value_len];

      for (int i = 0; i < _count; i++) {
	  new_value[i] = _value[i];
      }

      new_value[_count] = c;
      
      _value = new_value;
      _count = new_value_len;      
  }
}

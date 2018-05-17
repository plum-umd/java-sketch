package java.lang;

public class String {
    char[] _value;
    int _count;
    
    // use this constructor as it includes "count"
    // ignore offset at the moment
    public String(char[] ca, int offset, int count) {
    	if (offset > 0 && offset < ca.length) {
    	    char[] tmp = new char[count];
    	    for (int i=0; i<count; i++) {
    		tmp[i] = ca[i+offset];
    	    }
    	    _value = tmp;
    	}
    	else {
    	    _value = ca;
    	}
    	_count = count;	
    }

    // public char charAt(int index) {
    // 	if (0 <= index && index < _count) return _value[index];
    // 	return '\0';
    // }

    public int length() {
	return _count;
    }

    // public String concat(String str) {
    // 	int otherLen = str.length();
    // 	if (otherLen == 0) {
    // 	    return this;
    // 	}
    // 	int thisLen = this.length();
    // 	int totalLen = this.length() + otherLen;
    // 	char [] ret = new char[totalLen];

    // 	for (int i = 0; i < thisLen; i++) {
    // 	    ret[i] = this.charAt(i);
    // 	}
    // 	for (int i = thisLen; i < totalLen; i++) {
    // 	    ret[i] = str.charAt(i-thisLen);
    // 	}

    // 	return new String(ret, 0, totalLen);
    // }

    // Should be boolean but that isn't parsing right!
    public boolean equals(Object obj) {
	boolean isEqual = false;

	if (obj instanceof String) {
	    isEqual = true;
	    String s = (String)obj;
	  
	    int sLen = s.length();
	    int tLen = this.length();
	  
	    if (sLen != tLen) isEqual = false;
	  
	    for (int i=0; (i < sLen) && (isEqual == true); i++) {
		if (s._value[i] != this._value[i]) {
		    isEqual = false;
		}
	    }
	}

	return isEqual;
	// return s._value == this._value;
    }

}

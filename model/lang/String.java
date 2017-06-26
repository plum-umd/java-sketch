package java.lang;

public class String implements CharSequence{
    char[] _value;
    int _count;

    // public String(int[] ca, int offset, int count) {
    // 	if (offset > 0 && offset < count) {
    // 	    int l = count-offset-1;
    // 	    char[] tmp = new char[l];
    // 	    for (int i=0; i<l; i++) {
    // 		tmp[i] = (char) ca[i+offset];
    // 	    }
    // 	    _value = tmp;
    // 	    _count = l;
    // 	} else {
    // 	    char[] tmp = new char[count];
    // 	    for (int i=0; i<count; i++) {
    // 		tmp[i] = (char) ca[i];
    // 	    }
    // 	    _value = tmp;
    // 	    _count = count;
    // 	}
    // }
    
    // use this constructor as it includes "count"
    // ignore offset at the moment
    public String(char[] ca, int offset, int count) {
	if (offset > 0 && offset < count) {
	    char[] tmp = new char[count];
	    for (int i=offset; i<offset+count; i++) {
		tmp[i] = ca[i];
	    }
	    _value = tmp;
	} else {
	    _value = ca;
	}
	_count = count;	
    }

    public char charAt(int index) {
	if (0 <= index && index < _count) return _value[index];
	return '\0';
    }

    public int length() {
	return _count;
    }

    public String toString() {
	return this;
    }


    public void setCharAt(int i, char c) {
	_value[i] = c;
    }

    public int indexOf(String s) {
	return indexOf(s, 0);
    }

    public int indexOf(String s, int i) {
	int tLen = this.length();
	int sLen = s.length();
	int index = i;
	int mLen = 0;
	int j;
	if (i >= tLen || i < 0 || sLen == 0) {
	    return -1;
	}

	for (j = i; (j < tLen) && (mLen < sLen) && ((j-index) < sLen); ) {
	    if (this.charAt(j) != s.charAt(j-index)) {
		mLen = 0;
		index++;
		j = index;
	    } else {
		mLen++;
		j++;
	    }
	}

	if (mLen != sLen) {
	    index = -1;
	}
      
	return index;
    }

    public int indexOf(char c) {
	return indexOf(c, 0);
    }

    public int indexOf(char c, int i) {
	int len = this.length();
	int index = -1;
	if (i >= len || i < 0) {
	    return index;
	}

	for (int j = i; (j < len) && (index == -1); j++) {
	    if (this.charAt(j) == c) {
		index = j;
	    }
	}

	return index;
    }

    public int compareTo(String str) {
    	return compare(this.toString(), str);
    }

    public static int compare(String s1, String s2) {
    	int l1 = s1.length();
    	int l2 = s2.length();

    	if (l1 < l2) {
    	    return l1 - l2;
    	} else if (l1 > l2) {
    	    return l2 - l1;
    	} else {
    	    for (int i=0; i<l1; i++) {
    		char c1 = s1.charAt(i);
    		char c2 = s2.charAt(i);
    		if (c1 != c2) {
    		    return c1 - c2;
    		}
    	    }
    	    return 0;
    	}
    }
    
    public String concat(String str) {
	int otherLen = str.length();
	if (otherLen == 0) {
	    return this;
	}
	int thisLen = this.length();
	int totalLen = this.length() + otherLen;
	char [] ret = new char[totalLen];

	for (int i = 0; i < thisLen; i++) {
	    ret[i] = this.charAt(i);
	}
	for (int i = thisLen; i < totalLen; i++) {
	    ret[i] = str.charAt(i-thisLen);
	}

	return new String(ret, 0, totalLen);
    }

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

    public int hashCode() {
	int n = _count, hash = 0, temp = 0;
	if (n == 0) {
	    return 0;
	}

	for (int i = 0; i < n; i++) {
	    temp = this.charAt(i);
	    for (int j = 0; j < n-1-i; j++) {
		temp *= 31;
	    }
	    hash += temp;
	}
	
	return hash;
    }
    public String replace(char oldChar, char newChar) {
	if (oldChar != newChar) {
	    int len = _count;
	    int i = -1;
	    int stop = 0;
	    char[_count] val = _value;
	    while (++i < len) {
		if (val[i] == oldChar && stop == 0) {
		    stop = i;
		}
	    }
	    if (stop < len) {
		char[] buf = new char[len];
		for (int j = 0; j < stop; j++) {
		    buf[j] = val[j];
		}
		while (stop < len) {
		    char c = val[stop];
		    buf[stop] = (c == oldChar) ? newChar : c;
		    stop++;
		}
		return new String(buf, 0, len);
	    }
	}
	return this;
    }
}

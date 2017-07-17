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
	if (offset > 0 /*&& offset < count*/) {
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
	int lendiff = l1-l2;
	int smaller = l1;
	
    	if (l1 > l2) {
	    smaller = l2;
    	} else {
    	    for (int i=0; i<smaller; i++) {
    		char c1 = s1.charAt(i);
    		char c2 = s2.charAt(i);
    		if (c1 != c2) {
    		    return c1 - c2;
    		}
    	    }
	    if (lendiff != 0) return lendiff;
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

    public String substring(int beginIndex) {
	int subLen = _count - beginIndex;
	assert subLen > 0;
	return (beginIndex == 0) ? this : new String(_value, beginIndex, subLen);
    }

    public String substring(int beginIndex, int endIndex) {
    	assert beginIndex >= 0 && endIndex <= _count;
    	int subLen = endIndex - beginIndex;
    	assert subLen > 0;
    	return (beginIndex == 0 && endIndex == _count) ? this :
    	    new String(_value, beginIndex, subLen);
    }

    // public String[] split(String regex, int limit) {
    // 	int off = 0;
    // 	char ch = regex.charAt(0);
    // 	int next = indexOf(ch, off);
    // 	boolean limited = limit > 0;
    // 	boolean c = true;
    // 	ArrayList<String> list = new ArrayList<>();
    // 	while (indexOf(ch, off) != -1) {
    // 	    if (c) {
    // 		if (!limited || list.size() < limit - 1) {
    // 		    list.add(substring(off, next));
    // 		    off = next + 1;
    // 		    next = indexOf(ch, off);
    // 		}
    // 		else {    // last one
    // 		    list.add(substring(off, value.length));
    // 		    off = value.length;
    // 		    c = !c;
    // 		}
    // 	    }
    // 	}
    // 	// If no match was found, return this
    // 	if (off == 0)
    // 	    return new String[]{this};
	
    // 	// Add remaining segment
    // 	if (!limited || list.size() < limit)
    // 	    list.add(substring(off, value.length));
	
    // 	// Construct result
    // 	int resultSize = list.size();
    // 	if (limit == 0) {
    // 	    while (resultSize > 0 && list.get(resultSize - 1).length() == 0) {
    // 		resultSize--;
    // 	    }
    // 	}
    // 	String[] result = new String[resultSize];
    // 	return list.subList(0, resultSize).toArray(result);
    // }
    //     /* fastpath if the regex is a
    //      (1)one-char String and this character is not one of the
    //         RegEx's meta characters ".$|()[{^?*+\\", or
    //      (2)two-char String and the first char is the backslash and
    //         the second is not the ascii digit or ascii letter.
    //      */
    //     char ch = 0;
    //     if (((regex.value.length == 1 &&
    //          ".$|()[{^?*+\\".indexOf(ch = regex.charAt(0)) == -1) ||
    //          (regex.length() == 2 &&
    //           regex.charAt(0) == '\\' &&
    //           (((ch = regex.charAt(1))-'0')|('9'-ch)) < 0 &&
    //           ((ch-'a')|('z'-ch)) < 0 &&
    //           ((ch-'A')|('Z'-ch)) < 0)) &&
    //         (ch < Character.MIN_HIGH_SURROGATE ||
    //          ch > Character.MAX_LOW_SURROGATE))
    //     {
    //         int off = 0;
    //         int next = 0;
    //         boolean limited = limit > 0;
    //         ArrayList<String> list = new ArrayList<>();
    //         while ((next = indexOf(ch, off)) != -1) {
    //             if (!limited || list.size() < limit - 1) {
    //                 list.add(substring(off, next));
    //                 off = next + 1;
    //             } else {    // last one
    //                 //assert (list.size() == limit - 1);
    //                 list.add(substring(off, value.length));
    //                 off = value.length;
    //                 break;
    //             }
    //         }
    //         // If no match was found, return this
    //         if (off == 0)
    //             return new String[]{this};

    //         // Add remaining segment
    //         if (!limited || list.size() < limit)
    //             list.add(substring(off, value.length));

    //         // Construct result
    //         int resultSize = list.size();
    //         if (limit == 0) {
    //             while (resultSize > 0 && list.get(resultSize - 1).length() == 0) {
    //                 resultSize--;
    //             }
    //         }
    //         String[] result = new String[resultSize];
    //         return list.subList(0, resultSize).toArray(result);
    //     }
    //     return Pattern.compile(regex).split(this, limit);
    // }
}

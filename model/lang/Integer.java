package java.lang;

public class Integer extends Number {
    public static final int   MIN_VALUE;

    // public static int MAX_VALUE = 2147483647;
    public static final int   MAX_VALUE;

    private final int value;
    
    public Integer(int value) {
    	this.value = value;
	// this.MIN_VALUE = 0x80000000;
	// this.MAX_VALUE = 0x7fffffff;
    }

    public int intValue() {
    	return this.value;
    }

    public int compareTo(Integer anotherInteger) {
        return compare(this.value, anotherInteger.intValue());
    }

    public static int compare(int x, int y) {
        return (x < y) ? -1 : ((x == y) ? 0 : 1);
    }

    public boolean equals(Object obj) {
    	if (obj instanceof Integer) {
    	    return this.value == ((Integer)obj).intValue();
    	}
    	return false;
    }

    public String toString() {
    	return toString(this.value);
    }

    public static String toString(int i) {

    	if (i == 0) {
    	    return "0";
    	}

    	int index = 0, temp = i, j;
    	// Can they ever be bigger than 32? Don't think so
    	//    Could calculate length first if need be
    	char [32] ret = new char[32];
    	char [32] ret2 = new char[32];
    	char [] nums = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

    	if (temp < 0) {
    	    temp *= -1;
    	}

    	while (temp > 0) {
	    index++;
    	    ret[index] = nums[temp%10];
    	    temp /= 10;
    	}

    	// Seems to be causing problems 
    	if (i < 0) {
	    index++;
    	    ret[index] = '-';
    	}
       
    	int size = index;

    	for (j=0; j<size; j++) {
    	    ret2[j] = ret[index-1];
    	    index --;
    	}

    	// It's Here :/
    	return new String(ret2, 0, size);
    }

    public int hashCode() {
    	return value;
    }

    public static int parseInt(String s) {
    	char [] nums = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
	int len = s.length();
	int num = 0;
	int mult = 1;
	
	for (int i = len-1; i >= 0; i--) {
	    char c = s.charAt(i);
	    for (int j = 0; j < 10; j++) {
		if (c == nums[j]) {
		    num += mult * nums[j];
		}
	    }
	    if (i == 0 && c == '-') num *= -1;
	    mult *= 10;	    
	}

	return num;
    }

}

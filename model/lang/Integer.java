package java.lang;

public class Integer extends Number {
    
    public static final int   MIN_VALUE = 0x80000000;    

    public static final int   MAX_VALUE = 0x7fffffff;

    private final int value;

    public Integer(int value) {
	this.value = value;
    }

    public int intValue() {
	return this.value;
    }

    // CAUSES MAXIMUM RECURSION DEPTH??
    /*
    public float v() {
	float x = 0.0;
	return x;
	//return (float)(this.value);
    }
    */

    public int compareTo(Integer anotherInteger) {
        return compare(this.value, anotherInteger.intValue());
    }

    public static int compare(int x, int y) {
	// int ret = -1;

	// if (x > y) {
	//     ret = 1;
	// } else if (x == y) {
	//     ret = 0;
	// }

	// return ret;
	// TERNARY CAUSING PARSING ERROR?
        return (x < y) ? -1 : ((x == y) ? 0 : 1);
    }

    // Should take Object eventually 
    // ALSO SEEMS TO BE CAUSING A PARSING ERROR?
    // CHANGING TO INT SO IT CAN WORK!
    public boolean equals(Object anotherInt) {
	if (anotherInt instanceof Integer) {
	    Integer x = (Integer) anotherInt;
	    if (this.value == x.intValue()) {
		return true;
	    }
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
	    ret[index++] = nums[temp%10];
	    temp /= 10;
	}

	// Seems to be causing problems 
	if (i < 0) {
	    ret[index++] = '-';
	}
       
	int size = index;

	for (j=0; j<size; j++) {
	    ret2[j] = ret[index-1];
	    index --;
	}

	// It's Here :/
	return new String(ret2, 0, size);
    }

}

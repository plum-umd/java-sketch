package java.lang;

public class Float extends Number {

    private final float value;

    public Float(float value) {
	this.value = value;
    }

    public Float(double value) {
	this.value = value;
    }

    public float floatValue() {
	return this.value;
    }

    public int compareTo(Float anotherFloat) {
        return compare(this.value, anotherFloat.value);
    }

    // This might need to change, implementation different in source
    public static int compare(float x, float y) {
	// int ret = -1;

	// if (x > y) {
	//     ret = 1;
	// } else if (x == y) {
	//     ret = 0;
	// }

	// return ret;

        return (x < y) ? -1 : ((x == y) ? 0 : 1);
    }

    public boolean equals(Object anotherFloat) {
	if (anotherFloat instanceof Float) {
	    Float x = (Float) anotherFloat;
	    if (x.value == this.value) {
		return true;
	    }
	}
	return false;
    }

    public int intValue() {
	// return (int)this.value;
	return this.value;
    }

    public String toString() {
    	return toString(this.value);
    }

    public static String toString(float i) {
    	// int index = 0, j, temp2 = (int)i;
    	int index = 0, j, temp2 = i;
    	float temp = i - (float)((int)i);
    	char [32] ret = {
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0',
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0',
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0',
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0'
    	};
    	char [32] ret2 = {
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0',
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0',
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0',
    	    '\0', '\0', '\0', '\0','\0', '\0', '\0', '\0'
    	};
    	char [] nums = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

    	if (temp2 < 0) {
    	    temp2 *= -1;
    	}

	index++;
    	ret[index] = '.';

    	while (temp2 > 0) {
	    index++;
    	    ret[index] = nums[temp2%10];
    	    temp2 /= 10;
    	}

    	// Seems to be causing problems 
    	if (i < 0.0) {
	    index++;
    	    ret[index] = '-';
    	}
       
    	int size = index;

    	for (j=0; j<size; j++) {
    	    ret2[j] = ret[index-1];
    	    index --;
    	}

    	index = size;

    	while (temp > 0.0) {
    	    temp *= 10.0;
	    index++;
    	    ret2[index] = nums[(int)temp];
    	    temp = temp - (float)((int)temp);
    	}

    	return new String(ret2, 0, index);
    }

}

package java.lang;

public class Integer {
    private final int value;
    
    public Integer(int value) {
    	this.value = value;
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

    public int hashCode() {
	return this.value;
    }
}

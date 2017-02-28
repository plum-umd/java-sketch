class Objects extends Object {
    
    public static boolean equals(Object a, Object b) {
	if (a == null) {
	    if (b == null) {
		return true;
	    }
	    return false;
	}
	return a.equals(b);
    }

    public static int hashCode(Object o) {
        return o != null ? o.hashCode() : 0;
    }
}

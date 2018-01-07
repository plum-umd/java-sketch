class Boolean {

    boolean bool;
    
    public Boolean(boolean bool) {
	this.bool = bool;
    }

    boolean booleanValue() {
	return this.bool;
    }

    public String toString() {
	return toString(this.bool);
    }
    
    public static String toString(boolean bool) {
	if (bool) return "true";
	return "false";
    }	
}

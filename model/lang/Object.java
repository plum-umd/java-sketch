public class Object {

    public String toString() {
	return "Object toString()";
    }

    public boolean equals(Object obj) {
	return true;
    }

    // NOTE THAT THIS SHOULD BE OVERRIDDEN FOR ALL RELEVANT CLASSES
    public int hashCode() {
	return 0;
    }
}

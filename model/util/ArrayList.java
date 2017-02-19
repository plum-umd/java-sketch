package java.util;

public class ArrayList<E> {

    Object[] elementData;

    private int size;

    public ArrayList() {
	this.elementData = new Object[10];
    }

    public ArrayList(int initialCapacity) {
	this.elementData = new Object[initialCapacity];
    }

    // Should be a boolean
    public boolean add(E e) {
	return true;
    }

}


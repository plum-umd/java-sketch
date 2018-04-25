package java.util;

public class ArrayList<E> implements List<E>{

    Object[] elementData;

    private int DEFAULT_CAPACITY;
    private int capacity;
    private int size;
    private static Object[] EMPTY_ELEMENTDATA = {};
    private static final int MAX_ARRAY_SIZE = 1000000; // other value causing weird problem in Sketch
    // private static final int MAX_ARRAY_SIZE = 0x7fffffff - 8;

    public ArrayList() {
	this.DEFAULT_CAPACITY = 10;
	this.elementData = new Object[this.DEFAULT_CAPACITY];
	this.capacity = this.DEFAULT_CAPACITY;
	this.size = 0;
    }

    // Expand capacity to size while keeping old elements of elementData
    private void copyNewElementData(int size) {
	Object[] newElementData = new Object[size];
	int i = 0;

	for (i = 0; i < this.size; i++) {
	    newElementData[i] = elementData[i];
	}

	elementData = newElementData;
	capacity = size;
    }

    // if adding one would be out of bounds, expand elementData
    private void checkAdjustSize() {
	if (size + 1 >= capacity) {
	    // Arbitrarily 10, should compare to source
	    copyNewElementData(capacity + 10);
	}
    }

    private void createSpace(int index) {
	int j = 0;

	// Note - 1 because one after last element could be out of range
	for (j = size; j > index; j--) {
	    elementData[j] = elementData[j-1];
	}
    }

    public <E> boolean add(E e) {
    // public <E> boolean add(E e) {
	checkAdjustSize();
	elementData[size++] = e;
	return true;
    }

    public E get(int index) {
	if (index < 0 || index >= size) {
	    return null;
	}

	return elementData[index];
    }

    public int size() {
	return size;
    }
}


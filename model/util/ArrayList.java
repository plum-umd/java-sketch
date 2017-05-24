package java.util;

public class ArrayList<E> {

    Object[] elementData;

    private int DEFAULT_CAPACITY;
    private int numElements;
    private int capacity;
    private static Object[] EMPTY_ELEMENTDATA = {};
    private static final int MAX_ARRAY_SIZE = 1000000; // other value causing weird problem in Sketch
    // private static final int MAX_ARRAY_SIZE = 0x7fffffff - 8;

    public ArrayList() {
	this.elementData = new Object[10];
	this.capacity = 10;
	this.numElements = 0;
	this.DEFAULT_CAPACITY = 10;
    }

    public ArrayList(int initialCapacity) {
	this.elementData = new Object[initialCapacity];
	this.capacity = initialCapacity;	
	this.numElements = 0;
    }

    // Expand capacity to size while keeping old elements of elementData
    private void copyNewElementData(int size) {
	Object[] newElementData = new Object[size];
	int i = 0;

	for (i = 0; i < numElements; i++) {
	    newElementData[i] = elementData[i];
	}

	elementData = newElementData;
	capacity = size;
    }

    // if adding one would be out of bounds, expand elementData
    private void checkAdjustSize() {
	if (numElements + 1 >= capacity) {
	    // Arbitrarily 10, should compare to source
	    copyNewElementData(capacity + 10);
	}
    }

    private void createSpace(int index) {
	int j = 0;

	// Note - 1 because one after last element could be out of range
	for (j = numElements; j > index; j--) {
	    elementData[j] = elementData[j-1];
	}
    }

    public <E> void add(int index, E e) {
	checkAdjustSize();
	createSpace(index);
	elementData[index] = e;
	numElements ++;
    }

    public <E> boolean add(E e) {
	checkAdjustSize();
	elementData[numElements++] = e;
	return true;
    }

    public void clear() {
	// clear for GC
	for (int i = 0; i < numElements; i++) {
	    elementData[i] = null;
	}
	capacity = 10;
	numElements = 0;
    }

    public boolean contains(Object o) {
	return indexOf(o) >= 0;
    }

    public E get(int index) {
	if (index < 0 || index >= numElements) {
	    return null;
	}

	return elementData[index];
    }

    public int indexOf(Object o) {
	int i = 0;
	if (o == null) {
            for (i = 0; i < capacity; i++) {
                if (elementData[i]==null) {
                    return i;
		}
	    }
        } else {
            for (i = 0; i < numElements; i++) {
                if (o.equals(elementData[i])) {
                    return i;
		}
	    }
        }
        return -1;
    }

    private void removeElement(int index) {
	int j = 0;

	// Note - 1 because one after last element could be out of range
	for (j = index; j < numElements - 1; j++) {
	    elementData[j] = elementData[j+1];
	}
	elementData[numElements-1] = null;
	numElements --;
    }

    public E remove(int index) {
	E e;
	if (index < 0 || index >= numElements) {
	    return null;
	}	
	e = elementData[index];
	removeElement(index);
	return e;
    }

    public boolean remove(Object o) {
	int i = 0;
	if (o == null) {
            for (i = 0; i < capacity; i++) {
                if (elementData[i]==null) {
                    removeElement(i);
		    return true;
		}
	    }
        } else {
            for (i = 0; i < numElements; i++) {
                if (o.equals(elementData[i])) {
                    removeElement(i);
		    return true;
		}
	    }
        }
        return false;	
    }


    public <E> E set (int index, E element) {
	E oldElement;

	if (index < 0 || index >= numElements) {
	    return null;
	}

	oldElement = elementData[index];
	elementData[index] = element;

	return oldElement;
    }
    
    public int size() {
	return numElements;
    }

    public int length() {
	return size();
    }

    public boolean isEmpty() {
	return numElements == 0;
    }

    public Object[] toArray() {
	Object[] arr = new Object[numElements];
	int i = 0;

	for (i = 0; i < numElements; i++) {
	    arr[i] = elementData[i];
	}

	return arr;
    }
    public void ensureCapacity(int minCapacity) {
	int minExpand;
	if (elementData != EMPTY_ELEMENTDATA) { minExpand = 0; }
	else { minExpand = DEFAULT_CAPACITY; }
	assert minCapacity == 11;
	if (minCapacity > minExpand) { ensureExplicitCapacity(minCapacity); }
    }

    private void ensureCapacityInternal(int minCapacity) {
        if (elementData == EMPTY_ELEMENTDATA) {
	    if (DEFAULT_CAPACITY > minCapacity) { minCapacity = DEFAULT_CAPACITY; }
        }
	assert minCapacity == 11;
        ensureExplicitCapacity(minCapacity);
    }

    private void ensureExplicitCapacity(int minCapacity) {
        // modCount++; // What is this?

        // overflow-conscious code
        if (minCapacity - elementData.length > 0)
            grow(minCapacity);
    }

    private void grow(int minCapacity) {
	assert minCapacity == 11;
        // overflow-conscious code
        int oldCapacity = elementData.length;
        int newCapacity = oldCapacity + (oldCapacity / 2);
	assert newCapacity == 15;
        if (newCapacity - minCapacity < 0)
            newCapacity = minCapacity;
        if (newCapacity - MAX_ARRAY_SIZE > 0)
            newCapacity = hugeCapacity(minCapacity);
        // minCapacity is usually close to size, so this is a win:
	assert newCapacity == 15;
	copyNewElementData(newCapacity);
    }

    private static int hugeCapacity(int minCapacity) {
        return (minCapacity > MAX_ARRAY_SIZE) ?
            0x7fffffff :
            MAX_ARRAY_SIZE;
    }
}


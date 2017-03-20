class AbstractQueue<E> implements Queue {

    Object[] elementData;
    int size;
    int capacity;

    public AbstractQueue() {
	elementData = new Object[10];
	size = 0;
	capacity = 10;
    }

    private void resize() {
	if (size >= capacity) {
	    capacity *= 2;
	    Object[] newElementData = new Object[capacity];

	    for (int i = 0; i < size; i ++) {
		newElementData[i] = elementData[i];
		elementData[i] = null;
	    }

	    elementData = newElementData;
	}
    }

    public <E> boolean add(E e) {
	resize();
	size ++;
	elementData[size-1] = e;
    	return true;
    }

    public void clear() {
	for (int i = 0; i < size; i++) {
	    elementData[i] = null;
	} 
	elementData = new Object[10];
	size = 0;
	capacity = 10;
    }

    public E element() {
	if (size <= 0) {
	    return null;
	}
    	return elementData[0];
    }

    public E remove() {
	if (size <= 0) {
	    return null;
	}
	E e = elementData[0];
	for (int i = 0; i < size -1; i ++) {
	    elementData[i] = elementData[i+1];
	}
	elementData[size-1] = null;
	size --;
    	return e;
    }

}

package java.util;

public class Stack<E> extends Object{
    
    Object[] elementData;
    int size;
    int capacity;

    public Stack() { 
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

    public boolean empty() {
	return size == 0;
    }

    public E peek() {
	if (size <= 0) {
	    return null;
	}
	return elementData[size-1];
    }

    public <E> E push(E e) {
	resize();
	size ++;
	elementData[size-1] = e;
	return e;
    }

    public E pop() {
	if (size <= 0) {
	    return null;
	}
	E e = elementData[size-1];
	elementData[--size] = null;
	return e;
    }

    public <E> int search(Object o) {

	for (int i = 0; i < size; i++) {
	    if (elementData[i].equals(o)) {
		return i;
	    }
	}
	return -1;
    }
}

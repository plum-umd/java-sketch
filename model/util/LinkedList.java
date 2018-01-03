package java.util;

public class LinkedList<E> implements List<E> {
    public LinkedList() { };
    
    /* These are translated to uninterpreted functions in Sketch which doesn't work */
    public boolean add(E e) {
    // previous: public boolean add(Object e) 2017-11-13
    	return false;
    }
    public boolean isEmpty() {
    	return false;
    }
    public E get(int index) {
    	return null;
    }
    public void remove(Object e) {

    }
    public boolean remove(int index) {
    	return false;
    }

    public <E> E set (int index, E element) {
	return null;
    }

    public int size() {
	return 0;
    }
}

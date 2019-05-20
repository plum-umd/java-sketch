package java.util;

private class ArrayAsListIterator<E> implements Iterator<E> {
    private E[] es = null;
    private int index = -1;
    public ArrayAsListIterator(E[] es) {
        this.es = es;
    }
    public boolean hasNext() {
        Object[] es = this.es;
        return (this.index + 1) < es.length;
    }
    public E next() {
        if(hasNext()) {
            this.index++;
        } else {
            throw new NoSuchElementException();
            return null;
        }
        return this.es[this.index];
    }
    public void remove() {
        throw new UnsupportedOperationException();
    }
}

private class ArrayAsList<E> implements List<E> {
    private E[] es = null;
    public AsList(E[] es) {
        this.es = es;
    }
    public <E> boolean add(E e) {
        throw new UnsupportedOperationException();
        return false;
    }
    public boolean isEmpty() {
        return size() == 0;
    }
    public E get(int index) {
        return this.es[index];
    }
    public E remove(int index) {
        throw new UnsupportedOperationException();
        return null;
    }
    public boolean remove(Object e) {
        throw new UnsupportedOperationException();
        return false;
    }
    public <E> E set (int index, E element) {
        E old = this.es[index];
        this.es[index] = element;
        return old;
    }
    public int size() {
        Object[] es = this.es;
        return es.length;
    }
    public Iterator<E> iterator() {
        return new ArrayAsListIterator<E>(es);
    }
}

public class Arrays {

    public static byte[] copyOf(byte[] in, int len) {
	byte[] n = new byte[len];

	for (int i = 0; i < len; i++) {
	    if (i >= in.length) {
		n[i] = 0;
	    } else {
		n[i] = in[i];
	    }
	}
	return n;
    }

    // public static boolean equals(byte[] b1, byte[] b2) {    
    public static boolean arraysEquals(byte[] b1, byte[] b2) {
	if (b1.length == b2.length) {
	    for (int i = 0; i < b1.length; i++) {
		if (b1[i] != b2[i]) return false;
	    }
	} else {
	    return false;
	}
	return true;
    }

    public static <E> List<E> asList(E[] es) {
        return new ArrayAsList<E>(es);
    }
}

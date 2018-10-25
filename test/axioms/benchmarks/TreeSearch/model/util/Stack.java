public class Stack<E> {
    E[] elements;
    int CAPACITY;
    int RESIZE_FACTOR;
    int size;
    
    public Stack() {
	RESIZE_FACTOR = 2;
	CAPACITY = 8;
	elements = new E[CAPACITY];
	size = 0;
    }

    public void resize() {
	E[] new_elements = new E[CAPACITY*RESIZE_FACTOR];
	for (int i = 0; i < CAPACITY; i++) {
	    new_elements[i] = elements[i];
	}
	elements = new_elements;
	CAPACITY = CAPACITY * RESIZE_FACTOR;
    }

    public void push(E e) {
	if (size == CAPACITY) {
	    resize();
	}
	elements[size] = e;
	size++;
    }

    public E pop() {
	E e = elements[size-1];
	size--;
	return e;
    }

    public int size() {
	return size;
    }

    public boolean empty() {
	return size == 0;
    }
}

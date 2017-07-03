// THIS CLASS IS UNTESTED

public class ArrayDeque <E> implements Deque{

    public class DequeNode {
	E val;
	DequeNode prev;
	DequeNode next;

	public DequeNode(E v, DequeNode p, DequeNode n) {
	    val = v;
	    prev = p;
	    next = n;
	}

	public DequeNode getNext() {
	    return next;
	}

	public DequeNode getPrev() {
	    return prev;
	}

	public E getVal() {
	    return val;
	}
	
	public void setNext(DequeNode n) {
	    next = n;
	}

	public void setPrev(DequeNode p) {
	    prev = p;
	}
    }

    DequeNode currentHead;
    DequeNode currentTail;
    int size;
    
    public ArrayDeque() {
	currentHead = null;
	currentTail = null;
	size = 0;
    }

    public int size() {
	return size;
    }

    public boolean isEmpty() {
	return size == 0;
    }

    public boolean add(E e) {
	DequeNode newNode = new DequeNode(e, null, null);
	if (isEmpty()) {
	    currentHead = newNode;
	} else {
	    newNode.setPrev(currentTail);
	}
	currentTail = newNode;
	size++;
	return true;
    }

    public void addLast(E e) {
	add(e);
    }

    public void addFirst(E e) {
	DequeNode newNode = new DequeNode(e, null, null);
	if (isEmpty()) {
	    currentTail = newNode;
	} else {
	    newNode.setNext(currentHead);
	}
	currentHead = newNode;
	size++;
    }

    public int getIndex(Object o) {
	DequeNode current = currentHead;
	int index = 0;
	
	while (current != null) {
	    if (current.equals(o)) {
		return index;
	    }
	    index ++;
	    current = current.getNext();
	}
	return -1;
    }
    
    public boolean contains(Object o) {
	return getIndex(o) >= 0;
    }

    public E getFirst() {
	return currentHead;
    }

    public E getLast() {
	return currentTail;
    }

    public E peek() {
	return getFirst();
    }

    public E peekFirst() {
	return getFirst();
    }

    public E peekLast() {
	return getLast();
    }

    public E removeFirst() {
	DequeNode head = currentHead;
	if (currentHead != null) {
	    DequeNode nextNode = currentHead.getNext();
	    if (nextNode != null) {
		nextNode.setPrev(null);
	    }
	    currentHead = currentHead.next;
	    if (size == 1) {
		currentTail = null;
	    }
	    size --;
	}
	return head;
    }
	
    public E removeLast() {
	DequeNode tail = currentTail;
	if (currentTail != null) {
	    DequeNode prevNode = currentTail.getPrev();
	    if (prevNode != null) {
		prevNode.setNext(null);
	    }
	    currentTail = currentTail.prev;
	    if (size == 1) {
		currentHead = null;
	    }
	    size --;
	}
	return tail;
    }

    public E remove() {
	return removeFirst();
    }

    public boolean remove(Object o) {
	DequeNode current = currentHead;
	while (current != null) {
	    if (current.equals(o)) {
		DequeNode nextNode = current.getNext();
		DequeNode prevNode = current.getPrev();
		if (nextNode != null) {
		    nextNode.setPrev(null);
		}
		if (prevNode != null) {
		    prevNode.setNext(null);
		}
		if (current == currentHead) {
		    currentHead = currentHead.getNext();
		} else if (current == currentTail) {
		    currentTail = currentTail.getPrev();
		}
		return true;
	    }
	}
	return false;
    }
}

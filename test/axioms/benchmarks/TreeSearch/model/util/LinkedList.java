public class LinkedList<E> {

    public class Node<E> {
    	private Node next;
    	private E val;

    	public Node(Node next, E val) {
    	    this.next = next;
    	    this.val = val;
    	}

    	public void setNext(Node next) {
    	    this.next = next;
    	}

    	public boolean hasNext() {
    	    return this.next != null;
    	}

    	public Node<E> getNext() {
    	    return this.next;
    	}

	public E getVal() {
	    return val;
	}
    }

    int size;
    Node<E> head;
    
    public LinkedList() {
    	head = null;
    	size = 0;
    }

    public void add(E e) {
    	if (head == null) {
    	    head = new Node<E>(null, e);
    	} else {
    	    Node<E> n = head;
    	    while(n.hasNext()) {
    		n = n.getNext();
    	    }
    	    n.setNext(new Node<E>(null, e));
    	}
    }

    public int size() {
    	if (head == null) {
    	    return 0;
    	} else {
    	    Node<E> n = head;
    	    int sz = 1;
    	    while(n.hasNext()) {
    		n = n.getNext();
    		sz = sz + 1;
    	    }
    	    return sz;
    	}
    }

    public E get(int i) {
    	if (head == null) {
    	    return null;
    	} else {
    	    Node<E> n = head;
    	    int index = 0;
    	    while(n.hasNext()) {
		if (index == i) {
		    return n;
		}
		index = index + 1;
    		n = n.getNext();
    	    }
	    if (index == i) {
		return n;
	    }
    	    return null;
    	}
    }

    public E poll() {
	if (head == null) {
	    return null;
	} else {
	    E val = head.getVal();
	    head = head.getNext();
	    return val;
	}
    }
}

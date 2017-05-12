public class HashMap_NoHash<K,V> extends Map {

    Node elementData;
    int numPairs;

    class Node<K,V> extends Object {
	K key;
	V value;
	Node next;

	public Node(K key, V value, Node next) {
	    this.key = key;
	    this.value = value;
	    this.next = next;
	}
    }

    public HashMap_NoHash() {
	this.elementData = null;
    	this.numPairs = 0;
    }

    public int size() {
        return numPairs;
    }

    public boolean isEmpty() {
        return numPairs == 0;
    }

    public boolean containsValue(V value) {
	Node n = elementData;

	while (n != null) {
	    V v = n.value;
	    if (value.equals(v)) {
		return true;
	    }
	    n = n.next;
	}

	return false;
    }

    public boolean containsKey(K key) {
	return get(key) != null;
    }

    public V get(K key) {
	Node n = elementData;

	while (n != null) {
	    K k = n.key;
	    if (key.equals(k)) {
		return n.value;
	    }
	    n = n.next;
	}

	return null;
    }

    public void clear() {
	elementData = null;
	this.numPairs = 0;
    }

    public V remove(K key) {
	Node n = elementData, prev;
	V val = null;
	K k;

	if (n != null) {
	    k = n.key;
	    if (key.equals(k)) {
		val = n.value;
		elementData = n.next;
		numPairs --;
		return val;
	    }
	    prev = n;
	    n = n.next;
	}

	while (n != null) {
	    k = n.key;
	    if (key.equals(k)) {
		val = n.value;
		prev.next = n.next;
		numPairs --;
		return val;
	    }
	    n = n.next;
	}

	return null;
    }

    public V put(K key, V value) {
	Node n = elementData;
	V val = null;

	while (n != null) {
	    K k = n.key;
	    if (key.equals(k)) {
		val = n.value;
		n.value = value;
	    }
	    n = n.next;
	}

	if (val == null) {
	    Node newNode = new Node(key, value, elementData);	    
	    elementData = newNode;	    
	    numPairs++;
	}

	return val;
    }

}

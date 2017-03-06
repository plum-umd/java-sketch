public class HashMap_Simple<Integer,String> extends Object {

    static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
    Node[] elementData;
    int numPairs;
    int capacity;

    class Node<Integer,String> extends Object implements Map.Entry<Integer,String> {
	Integer key;
	String value;
	int hash;

	public Node(Integer key, String value, int hash) {
	    this.key = key;
	    this.value = value;
	    this.hash = hash;
	}
    }

    public HashMap_Simple() {
	this.elementData = new Node[DEFAULT_INITIAL_CAPACITY];
    	this.numPairs = 0;
	this.capacity = DEFAULT_INITIAL_CAPACITY;
    }

    public int size() {
        return numPairs;
    }

    public boolean isEmpty() {
        return numPairs == 0;
    }

    public void resize(int newSize) {
	int i,h, hashMod;
	Node<Integer, String> n;
	Node[] oldElementData = elementData;
	Node[] newElementData = new Node[newSize];
	//this.elementData = new Node[newSize];
	Integer k;
	String v;

	for (i = 0; i < capacity; i++) {
	    // putVal call gives Sketch Not Resolved Error
	    if (oldElementData[i] != null) {
		h = oldElementData[i].hash;
		k = oldElementData[i].key;
		v = oldElementData[i].value;
		//putValNoResize(h, k, v);
		hashMod = h % newSize;
		newElementData[hashMod] = new Node<Integer,String>(k, v, h);
	    }
	}

	this.elementData = newElementData;
	this.capacity = newSize;
    }

    public boolean containsValue(String value) {
	int i;

	for (i = 0; i < capacity; i++) {
	    if (elementData[i] != null) {
		String v = elementData[i].value;
		if (value.equals(v)) {
		    return true;
		}
	    }
	}
	return false;
    }

    public boolean containsKey(Integer key) {
	return get(key) != null;
    }

    public String get(Integer key) {
	int hashMod = key.hashCode() % capacity;
	Node<Integer,String> node = elementData[hashMod];

	if (node != null) {
	    if (key.equals(node.key)) {
		return node.value;
	    }
	}
	return null;
    }

    public void clear() {
	elementData = new Node[DEFAULT_INITIAL_CAPACITY];
	this.capacity = DEFAULT_INITIAL_CAPACITY;
	this.numPairs = 0;
    }

    public String remove(Integer key) {
	String val = get(key);
	int hashMod = key.hashCode() % capacity;

	elementData[hashMod] = null;

	if (val != null) {
	    numPairs --;
	}

	return val;
    }

    public String put(Integer key, String value) {
	int h = key.hashCode();
        return putVal(h, key, value);
    }

    private String putVal(int hash, Integer key, String value) {
	int hashMod = hash % capacity;
	Node<Integer,String> node = elementData[hashMod];
	
	if (node != null) {
	    if (node.hash != hash || !key.equals(node.key)) {
		resize(hash+1);
		hashMod = hash % capacity;
		node = elementData[hashMod];
		numPairs ++;
	    } 
	    elementData[hashMod] = new Node<Integer,String>(key, value, hash);
	    if (node != null) {
		return node.value;
	    } else {
		return null;
	    }
	}
	elementData[hashMod] = new Node<Integer,String>(key, value, hash);
	numPairs ++;
	return null;
    }

    private void putValNoResize(int hash, Integer key, String value) {
	int hashMod = hash % capacity;

	elementData[hashMod] = new Node<Integer,String>(key, value, hash);
    }

}

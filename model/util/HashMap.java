// public class HashMap<K,V> extends Map {
public class HashMap<K,V> {
    static final int DEFAULT_INITIAL_CAPACITY;// = 1 << 4; // aka 16
    Node[] elementData;
    int numPairs;
    int capacity;

    class Node<K,V> extends Object {
    	K key;
    	V value;
    	int hash;

    	public Node(K key, V value, int hash) {
    	    this.key = key;
    	    this.value = value;
    	    this.hash = hash;
    	}
    }

    public HashMap() {
	this.DEFAULT_INITIAL_CAPACITY = 16;
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
    	Node<K, V> n;
    	Node[] oldElementData = elementData;
    	Node[] newElementData = new Node[newSize];
    	//this.elementData = new Node[newSize];
    	K k;
    	V v;

    	for (i = 0; i < capacity; i++) {
    	    // putVal call gives Sketch Not Resolved Error
    	    if (oldElementData[i] != null) {
    		h = oldElementData[i].hash;
    		k = oldElementData[i].key;
    		v = oldElementData[i].value;
    		//putValNoResize(h, k, v);
    		hashMod = h % newSize;
    		if (hashMod < 0) {
    		    hashMod += newSize;
    		}
    		newElementData[hashMod] = new Node<K,V>(k, v, h);
    	    }
    	}

    	this.elementData = newElementData;
    	this.capacity = newSize;
    }

    public boolean containsValue(V value) {
    	int i;

    	for (i = 0; i < capacity; i++) {
    	    if (elementData[i] != null) {
    		V v = elementData[i].value;
    		if (value.equals(v)) {
    		    return true;
    		}
    	    }
    	}
    	return false;
    }

    public boolean containsKey(K key) {
    	return get(key) != null;
    }

    public V get(K key) {
    	int hashMod = key.hashCode() % capacity;
    	if (hashMod < 0) {
    	    hashMod += capacity;
    	}
    	Node<K,V> node = elementData[hashMod];

    	if (node != null) {
    	    if (key.equals(node.key)) {
    		return node.value;
    	    }
    	}
    	return null;
    }

    
    // public K[] keySet(K key) {
    // 	K[] keys = new K[size()];
    // 	for (int i = 0; i < size(); i++) keys[i] = elementData[i].key;
    // 	return keys;
    // }

    public void clear() {
    	elementData = new Node[DEFAULT_INITIAL_CAPACITY];
    	this.capacity = DEFAULT_INITIAL_CAPACITY;
    	this.numPairs = 0;
    }

    public V remove(K key) {
    	V val = get(key);
    	int hashMod = key.hashCode() % capacity;
    	if (hashMod < 0) {
    	    hashMod += capacity;
    	}

    	elementData[hashMod] = null;

    	if (val != null) {
    	    numPairs --;
    	}

    	return val;
    }

    public V put(K key, V value) {
    	int h = key.hashCode();
        return putVal(h, key, value);
    }

    public V replace(K key, V newVal) {
    	int hashMod = key.hashCode() % capacity;
    	if (hashMod < 0) {
    	    hashMod += capacity;
    	}
    	Node<K,V> node = elementData[hashMod];

    	if (node != null) {
    	    if (key.equals(node.key)) {
    		node.value = newVal;
    		return node.value;
    	    }
    	}
    	return null;
    }

    private V putVal(int hash, K key, V value) {
    	int hashMod = hash % capacity;
    	if (hashMod < 0) {
    	    hashMod += capacity;
    	}
    	Node<K,V> node = elementData[hashMod];
	
    	if (node != null) {
    	    if (node.hash != hash || !key.equals(node.key)) {
    		resize(hash+1);
    		hashMod = hash % capacity;
    		if (hashMod < 0) {
    		    hashMod += capacity;
    		}
    		node = elementData[hashMod];
    		numPairs ++;
    	    } 
    	    elementData[hashMod] = new Node<K,V>(key, value, hash);
    	    if (node != null) {
    		return node.value;
    	    } else {
    		return null;
    	    }
    	}
    	elementData[hashMod] = new Node<K,V>(key, value, hash);
    	numPairs ++;
    	return null;
    }

    private void putValNoResize(int hash, K key, V value) {
    	int hashMod = hash % capacity;
    	if (hashMod < 0) {
    	    hashMod += capacity;
    	}

    	elementData[hashMod] = new Node<K,V>(key, value, hash);
    }
}

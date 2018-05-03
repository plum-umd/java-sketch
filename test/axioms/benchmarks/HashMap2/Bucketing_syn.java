package HashingTechnique;

import java.util.ArrayList;

import Interfaing.HashTable;

public class Bucketing<K, V> implements HashTable<K, V> {
    private Pair<K, V>[] bucketHash;
    private ArrayList<Pair<K, V>> overflow;
    private int[] sizeBucket;
    private int numberOfElements;
    private int index, integerKey;
    private int size;
    private int mod, numberOfSlots;
    private ArrayList<K> ilterator;
    double rehash;

    // mod 10
    // 10 bucket
    public Bucketing() {
	size = 4; // 100
	mod = 2; 
	numberOfSlots = 2; // 10
	bucketHash = new Pair[size];
	overflow = new ArrayList<>();
	sizeBucket = new int[2];
	numberOfElements = 0;
    }

    public int sizeOfArray() {
	return size;
    }

    public void rehashng() {
    	ArrayList<Pair<K, V>> temp1 = new ArrayList<>();

    	// for (int i = ??; i < ??; i++) {
    	for (int i = 0; i < 2; i++) {
	    // int szbkt = sizeBucket[i];
	    // int g1 = {| szbkt , size, mod, numberOfSlots, numberOfElements |};
    	    for (int j = 0; j < sizeBucket[i]; j++) {
    		int index = i * numberOfSlots + j;
    		temp1.add(new Pair(bucketHash[index].key,bucketHash[index].value));
    	    }
    	}
	int sz = overflow.size();
	// int g2 = {| size, mod, numberOfSlots, numberOfElements, sz |};   
    	for (int i = 0; i < sz; i++) {
	    Pair<K,V> tmp = overflow.get(i);
	    temp1.add(tmp);
    	}

    	// size *= ??;
    	// numberOfSlots *= ??;
    	// mod *= ??;
    	size *= 4;
    	numberOfSlots *= 2;
    	mod *= 2;
    	bucketHash = new Pair[size];
    	sizeBucket = new int[mod];
    	numberOfElements = ??;

	int sz2 = temp1.size();
	// int g3 = {| size, mod, numberOfSlots, numberOfElements, sz2 |};   	
    	// for (int i = ??; i < temp1.size(); i++) {
    	for (int i = 0; i < sz2; i++) {
	    Pair<K,V> tmp = temp1.get(i);
	    K key = tmp.key;
	    V val = tmp.value;			
	    put(key, val);
    	}
    }

    public void put(K key, V value) {
	delete(key);
    	integerKey = key.hashCode() % mod;
	if (integerKey < ??) { integerKey *= ??; }

    	// check if there is a place in buckting array or not
    	if (sizeBucket[integerKey] != numberOfSlots) {
    	    int index = numberOfSlots * integerKey + sizeBucket[integerKey];
    	    bucketHash[index] = new Pair(key, value);
    	    sizeBucket[integerKey] = sizeBucket[integerKey] + 1;

    	}
	else {
    	    overflow.add(new Pair(key, value));
    	}
    	numberOfElements++;
    	rehash = (double) numberOfElements / (double) size;
    	if (rehash > 0.75)
    	    rehashng();
    }

    public V get(K key) {
	if (key == null) return null;
    	integerKey = key.hashCode() % mod;
	if (integerKey < ??) { integerKey *= ??; }

    	index = numberOfSlots * integerKey;
	int g3 = {| size, mod, numberOfSlots, numberOfElements, integerKey, index |};
	int add = index + sizeBucket[integerKey];
	int g4 = {| size, mod, numberOfSlots, numberOfElements, integerKey, index, add |}; 
    	for (int i = g3; i < g4; i++) {
	    Pair<K,V> tmp = bucketHash[i];
	    K tmp_key = tmp.key;
	    boolean b = tmp_key.equals(key);
	    if ({| b, tmp_key == key |}) { return tmp.value; }
    	}
    	if (sizeBucket[integerKey] == numberOfSlots) {
	    int sz = overflow.size();
	    int g5 = {| size, mod, numberOfSlots, numberOfElements, integerKey, index, sz |};	    
    	    for (int i = ??; i < g5; i++) {
		Pair<K,V> tmp = overflow.get(i);
		K tmp_key = tmp.key;				
		boolean b = tmp_key.equals(key);
		if ({| b, tmp_key == key |}) { return tmp.value; }
    	    }
    	}
    	return null;
    }
    
    public void delete(K key) {
    	integerKey = key.hashCode() % mod;
	if (integerKey < ??) { integerKey *= ??; }

    	index = numberOfSlots * integerKey;
    	boolean flag = false;
	int g3 = {| size, mod, numberOfSlots, numberOfElements, integerKey, index |};
	int add = index + sizeBucket[integerKey];	
	int g4 = {| size, mod, numberOfSlots, numberOfElements, integerKey, index, add |}; 

    	for (int i = g3; i < g4; i++) {
	    Pair<K,V> tmp = bucketHash[i];
	    K tmp_key = tmp.key;
	    boolean b = tmp_key.equals(key);
	    if ({| b, tmp_key == key |}) { 
    	    // if (tmp_key.equals(key)) {
		flag = true;
	    }
	    else if (flag) {
    		bucketHash[i-??] = new Pair(bucketHash[i].key, bucketHash[i].value);
    	    }
    	}
    	if (flag) {
    	    numberOfElements--;
    	    sizeBucket[integerKey] = sizeBucket[integerKey] - 1;
    	}
	else if (sizeBucket[integerKey] == numberOfSlots) {
	    int sz = overflow.size();
	    int g5 = {| size, mod, numberOfSlots, numberOfElements, integerKey, index, sz |};
    	    for (int i = ??; i < g5; i++) {
	    	Pair<K,V> tmp = overflow.get(i);
	    	K tmp_key = tmp.key;				
	    	boolean b = tmp_key.equals(key);
	    	if ({| b, tmp_key == key |}) { 
    	    	// if (tmp_key.equals(key)) {
    	    	    overflow.remove(i);
    	    	    numberOfElements--;
	    	    return;
    	    	}
    	    }
    	}
    }

    public boolean containsKey(K key) {
    	V check = get(key);
    	if (check == null)
    	    return false;
    	return true;
    }

    public boolean isEmpty() {
    	if (numberOfElements == ??)
    	    return true;
    	return false;
    }

    public int size() {
    	return numberOfElements;
    }

    // ADDED THIS FUNCTION TO HELP WITH TESTING
    public void clear() {
	bucketHash = new Pair[size];
	overflow = new ArrayList<>();
	sizeBucket = new int[2];
	numberOfElements = 0;
    }
    // public Iterable<K> keys() {
    // 	ilterator = new ArrayList();
    // 	for (int i = 0; i < 10; i++) {
    // 	    for (int j = 0; j < sizeBucket[i]; j++) {
    // 		int index = i * numberOfSlots + j;
    // 		ilterator.add(bucketHash[index].key);

    // 	    }
    // 	}
    // 	for (int i = 0; i < overflow.size(); i++) {
    // 	    ilterator.add(overflow.get(i).key);

    // 	}
    // 	return ilterator;
    // }
}

/********* ORIGINAL ************/
// package HashingTechnique;

// import java.util.ArrayList;

// import Interfaing.HashTable;

// public class Bucketing<K, V> implements HashTable<K, V> {

// 	private Pair<K, V> bucketHash[];
// 	private ArrayList<Pair<K, V>> overflow;
// 	private int sizeBucket[];
// 	private int numberOfElements;
// 	private int index, integerkey;
// 	private int size;
// 	private int mod, numberOfSlots;
// 	private ArrayList<K> ilterator;
// 	double rehash;

// 	// mod 10
// 	// 10 bucket
// 	public Bucketing() {
// 		size = 100;
// 		mod = 10;
// 		numberOfSlots = 10;
// 		bucketHash = new Pair[size];
// 		overflow = new ArrayList();
// 		sizeBucket = new int[10];
// 		numberOfElements = 0;

// 	}

// 	public int sizeOfArray() {
// 		return size;
// 	}

// 	public void rehashng() {

// 		ArrayList<Pair<K, V>> temp1 = new ArrayList();

// 		for (int i = 0; i < 10; i++) {
// 			for (int j = 0; j < sizeBucket[i]; j++) {

// 				int index = i * numberOfSlots + j;
// 				temp1.add(new Pair(bucketHash[index].key,
// 						bucketHash[index].value));
// 			}
// 		}
// 		for (int i = 0; i < overflow.size(); i++) {
// 			temp1.add(overflow.get(i));
// 		}

// 		size *= 4;
// 		numberOfSlots *= 2;
// 		mod *= 2;
// 		bucketHash = new Pair[size];
// 		sizeBucket = new int[mod];
// 		numberOfElements = 0;

// 		for (int i = 0; i < temp1.size(); i++) {
// 			put(temp1.get(i).key, temp1.get(i).value);

// 		}

// 	}

// 	@Override
// 	public void put(K key, V value) {
// 		delete(key);
// 		integerkey = Math.abs(key.hashCode() % mod);
// 		// check if there is a place in buckting array or not
// 		if (sizeBucket[integerkey] != numberOfSlots) {
// 			int index = numberOfSlots * integerkey + sizeBucket[integerkey];
// 			bucketHash[index] = new Pair(key, value);
// 			sizeBucket[integerkey]++;

// 		} else {
// 			overflow.add(new Pair(key, value));
// 		}
// 		numberOfElements++;
// 		rehash = (double) numberOfElements / (double) size;
// 		if (rehash > 0.75)
// 			rehashng();

// 	}

// 	@Override
// 	public V get(K key) {
// 		integerkey = Math.abs(key.hashCode() % mod);
// 		index = numberOfSlots * integerkey;
// 		for (int i = index; i < index + sizeBucket[integerkey]; i++) {
// 			if (bucketHash[i].key.equals(key))
// 				return bucketHash[i].value;
// 		}
// 		if (sizeBucket[integerkey] == numberOfSlots) {
// 			for (int i = 0; i < overflow.size(); i++) {
// 				if (overflow.get(i).key.equals(key))
// 					return overflow.get(i).value;
// 			}
// 		}
// 		return null;
// 	}

// 	@Override
// 	public void delete(K key) {
// 		integerkey = Math.abs(key.hashCode() % mod);
// 		index = numberOfSlots * integerkey;
// 		boolean flag = false;

// 		for (int i = index; i < index + sizeBucket[integerkey]; i++) {
// 			if (bucketHash[i].key.equals(key)) {
// 				flag = true;
// 			} else if (flag) {
// 				bucketHash[i - 1] = new Pair(bucketHash[i].key,
// 						bucketHash[i].value);

// 			}
// 		}
// 		if (flag) {
// 			numberOfElements--;
// 			sizeBucket[integerkey]--;
// 		} else if (sizeBucket[integerkey] == numberOfSlots) {
// 			for (int i = 0; i < overflow.size(); i++) {
// 				if (overflow.get(i).key.equals(key)) {
// 					overflow.remove(i);
// 					numberOfElements--;
// 					break;
// 				}
// 			}
// 		}

// 	}

// 	@Override
// 	public boolean contains(K key) {
// 		V check = get(key);
// 		if (check == null)
// 			return false;
// 		return true;
// 	}

// 	@Override
// 	public boolean isEmpty() {
// 		if (numberOfElements == 0)
// 			return true;
// 		return false;
// 	}

// 	@Override
// 	public int size() {

// 		return numberOfElements;
// 	}

// 	@Override
// 	public Iterable<K> keys() {
// 		ilterator = new ArrayList();
// 		for (int i = 0; i < 10; i++) {
// 			for (int j = 0; j < sizeBucket[i]; j++) {
// 				int index = i * numberOfSlots + j;
// 				ilterator.add(bucketHash[index].key);

// 			}
// 		}
// 		for (int i = 0; i < overflow.size(); i++) {
// 			ilterator.add(overflow.get(i).key);

// 		}
// 		return ilterator;
// 	}

// }

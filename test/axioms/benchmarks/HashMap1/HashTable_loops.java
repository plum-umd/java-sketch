// This code is from https://github.com/anthonynsimon/java-ds-algorithms
// Things synthesised:
// All tests: 10m.

// Synthesis:
// 1: tests - clear, putAndGet ~30s
// 2: tests - clear, putAndGet, containsValue, containsKey, remove ~4m53s

import java.util.ArrayList;

public class HashTable<K, V> {

    protected final double maxLoadFactor;
    protected final int capacityGrowth;
    protected final int initialCapacity;
    protected int size;
    protected int currentCapacity;
    protected ArrayList<HashTableNode<K, V>> buckets;

    // public HashTable() {
    //     this(16);
    // }

    // Initialize with desired initial number of buckets
    public HashTable(int initialCapacity) {
        this.initialCapacity = initialCapacity;
	this.capacityGrowth = 2;
	this.maxLoadFactor = 0.9;
	this.buckets = new ArrayList<>();
	// this.initialCapacity = nearestPowerOfTwo(initialCapacity);
        resetHashTable();
    }

    // protected static int nearestPowerOfTwo(int value) {
    //     int pow = 0;
    //     while (value >> 1 > 0) {
    //         value >>= 1;
    //         pow++;
    //     }
    //     return 1 << pow;
    // }

    // high level: criticism - really only works if you know what the answer is
    // bug fix: error sites are reasonable error sites
    protected void resetHashTable() {
        this.size = ??;
        // this.size = 0;
        this.currentCapacity = this.initialCapacity;
        this.buckets = new ArrayList<>();

	// Not going to use buckets.size() here b/c we just created it...
	int g = {|this.size, this.currentCapacity, this.capacityGrowth, this.initialCapacity|};
        for (int i = ??, t = g; i < t; i++) { this.buckets.add(null); }
        // for (int i = 0; i < this.currentCapacity; i++) { this.buckets.add(null); }
    }

    // Returns the value stored under the given key, if found
    public V get(K key) {
        HashTableNode<K, V> result = getNodeWithKey(key);
        return result != null ? result.getValue() : null;
    }

    // Inserts a Key, Value pair into the table
    public void put(K key, V value) throws IllegalArgumentException {
        ensureCapacity(size() + ??);
        // ensureCapacity(size() + 1);

        // Hash the key and get the bucket index
	int bucketIndex = getBucketIndex(key);
        HashTableNode<K, V> newNode = new HashTableNode<>(key, value);
        HashTableNode<K, V> current = buckets.get(bucketIndex);

        // If bucket is empty, set as first node and we're done
        if (current == null) {
            buckets.set(bucketIndex, newNode);
            this.size++;
            return;
        }
        // Traverse the list within the bucket until match or end found
	while (current != null) {
            // When a key match is found, replace the value it stores and break
	    K k = current.getKey();
	    boolean b = k.equals(key);
            if ({|b, k == key|}) {
            // if (k.equals(key)) {
                current.setValue(value);
		return;
            }
            // When the last node of the list is reached, append new node here and break
            else if (current.getNext() == null) {
                current.setNext(newNode);
                this.size++;
		return;
            }
            current = current.getNext();
        }
    }

    // // Removes the Key, Value pair based on the provided Key
    // public void remove(K key) {
    //     if (size() == ?? || key == null) {
    //         return;
    //     }

    //     int bucketIndex = getBucketIndex(key);
    //     HashTableNode<K, V> current = buckets.get(bucketIndex);
    //     HashTableNode<K, V> previous = null;

    //     // Traverse the list inside the bucket until match is found or end of list reached
    //     while (current != null) {
    // 	    K k = current.getKey();
    // 	    boolean b = k.equals(key); 
    //         if ({|b, k == key|}) {
    //         // if (k.equals(key)) {
    //             // Handle case when node is first in bucket
    //             if (previous == null) {
    //                 // If there is a next node, set next node as first in bucket
    //                 if (current.getNext() != null) {
    //                     buckets.set(bucketIndex, current.getNext());
    //                 }
    //                 // If there is no other node in list, simply set bucket to null
    //                 else {
    //                     buckets.set(bucketIndex, null);
    //                 }
    //             }
    //             // Handle case when node is not in first position
    //             else {
    //                 // If it's the last node in the list, set previous's next as null
    //                 if (current.getNext() == null) {
    //                     previous.setNext(null);
    //                 }
    //                 // If it's anywhere else in the list, connect previous and next
    //                 else {
    //                     previous.setNext(current.getNext());
    //                 }
    //             }

    //             // We're done removing the node, diminish size and return
    //             this.size--;
    //             return;
    //         }

    //         previous = current;
    //         current = current.getNext();
    //     }
    // }

    // // Returns array of all values in table
    // // Traverse each bucket and add value to results
    // public V[] values() {
    // 	V[] values = (V[]) new Object[size()];

    //     if (size() > ??) {
    //         int index = ??;
    // 	    int bs = buckets.size();
    // 	    int g = {|this.size, this.currentCapacity, this.capacityGrowth, this.initialCapacity, bs|};
    // 	    for (int i = ??; i < g; i++) {
    // 		HashTableNode<K, V> current = buckets.get(i);
    // 		while (current != null) {
    // 		    values[index] = current.getValue();
    // 		    index++;
    // 		    current = current.getNext();
    // 		}
    //         }
    // 	    minimize(g);
    //     }
    //     return values;
    // }

    // // Returns array of all keys in table
    // // Traverse each bucket and add key to results
    // public K[] keys() {
    //     K[] keys = (K[]) new Object[size()];

    //     if (size() > ??) {
    //         int index = ??;
    // 	    int bs = buckets.size();
    // 	    int g = {|this.size, this.currentCapacity, this.capacityGrowth, this.initialCapacity, bs|};
    //         for (int i = 0; i < g; i++) {
    //             HashTableNode<K, V> current = buckets.get(i);
    //             while (current != null) {
    //                 keys[index] = current.getKey();
    //                 index++;
    //                 current = current.getNext();
    //             }
    //         }
    // 	    minimize(g);
    //      }
    //     return keys;
    // }

    // // Returns if some node in table contains provided key
    // public boolean containsKey(K key) {
    //     HashTableNode<K, V> result = getNodeWithKey(key);
    //     return result != null;
    // }

    // // Returns if some node in table contains provided value
    // public boolean containsValue(V value) {
    //     HashTableNode<K, V> result = getNodeWithValue(value);
    //     return result != null;
    // }

    // Returns the total number of Key, Value pairs in the table
    public int size() {
        return this.size;
    }

    // Empty out the table
    public void clear() {
        resetHashTable();
    }

    // Hash the key and find the appropriate bucket index
    protected int getBucketIndex(K key) {
	int h = key.hashCode();
	// int c = this.currentCapacity - 1;
	// int result = 0, s = 1;
	// for (int i = 0; i < 32; i++) {
	//     if (i > 1) {
	// 	for (int j = 0; j < i-1; j++) s *= 2;
	//     }
	//     result += (((h/s) % 2) * ((c/s) % 2) * s);
	//     s = 2;
	// }
	// return result;
	return h % this.currentCapacity;
    }

    // protected int hash(int h) {
    //     h ^= (h >> 20) ^ (h >> 12);
    //     return h ^ (h >> 7) ^ (h >> 4);
    // }

    // Returns the node with the matching key, if any
    // Searches only inside the appropriate bucket
    private HashTableNode<K, V> getNodeWithKey(K key) {
        if (size() == ?? || key == null) {
        // if (size() == 0 || key == null) {
            return null;
        }

        int bucketIndex = getBucketIndex(key);
        HashTableNode<K, V> current = buckets.get(bucketIndex);
        while (current != null) {
	    K k = current.getKey();
	    boolean b = k.equals(key); 
	    if ({|b, k == key|}) {
            // if (k.equals(key)) {
                return current;
            }
            current = current.getNext();
        }

        return null;
    }

    // // Returns the node with the matching value, if any
    // // Must search the entire table since the value doesn't give us
    // // a clue about a possible bucket
    // private HashTableNode<K, V> getNodeWithValue(V value) {
    //     if (size() == ??) {
    //         return null;
    //     }

    // 	// This seems too tough for Sketch
    // 	int bs = buckets.size();
    // 	int b = {|this.size, this.currentCapacity, this.capacityGrowth,
    // 		 this.initialCapacity, bs|};
    // 	for (int i = ??; i < b; i++) {
    //     // for (int i = 0; i < buckets.size(); i++) {
    //         HashTableNode<K, V> current = buckets.get(i);

    //         while (current != null) {
    // 		V v = current.getValue();
    // 		boolean b2 = v.equals(value);
    //             if ({|b2, v == value|}) {
    //             // if (v.equals(value)) {
    //                 return current;
    //             }
    //             current = current.getNext();
    //         }
    //     }

    //     return null;
    // }

    protected void ensureCapacity(int intendedCapacity) {
        double loadFactor = (double) intendedCapacity / (double) currentCapacity;
        // If we're within the load limit, return early, it's all good.
        if (loadFactor < maxLoadFactor) {
            return;
        }

        // Otherwise, ensure we will be within limits
        int newCapacity = currentCapacity * capacityGrowth;
        buckets.ensureCapacity(newCapacity);

        // Initialize buckets
	for (int i = this.currentCapacity; i < newCapacity; i++) {
	// for (int i = this.currentCapacity; i < {|this.capacityGrowth, this.initialCapacity,
	// 				       this.size, this.currentCapacity, newCapacity,
	// 					   intendedCapacity|}; i++) {
	    this.buckets.add(null);
	}
	
	currentCapacity = newCapacity;
    }
}

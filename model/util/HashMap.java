public class HashMap<K,V>  {

    static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
    static final int MAXIMUM_CAPACITY = 1 << 30;
    static final float DEFAULT_LOAD_FACTOR = 0.75;
    static final int TREEIFY_THRESHOLD = 8;
    static final int UNTREEIFY_THRESHOLD = 6;
    static final int MIN_TREEIFY_CAPACITY = 64;

    transient Node<K,V>[] table;
    transient Set<Map.Entry<K,V>> entrySet;
    transient int size;

    transient int modCount;
    final float loadFactor;

    int threshold;
    // changing numPairs to "size" causes problems
    int numPairs;

    // public HashMap() {
    //     this.loadFactor = DEFAULT_LOAD_FACTOR;
    // 	this.threshold = DEFAULT_INITIAL_CAPACITY;
    // 	this.numPairs = 0;
    // }

    // public int size() {
    //     return numPairs;
    // }

    public boolean isEmpty() {
        return numPairs == 0;
    }

    // public boolean containsKey(Object key) {
    //     return getNode(hash(key), key) != null;
    // }

    // public boolean containsValue(Object value) {
    // 	return false;
    // }
    
    // final Node<K,V> getNode(int hash, Object key) {
    // 	Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    	// int len = tab.length;

    // 	//if ((tab = table) != null && (n = tab.length) > 0 &&
    // 	//    (first = tab[(n - 1) & hash]) != null) {
    // 	if (table) { tab = table; }
    // 	else { return null; }
    // 	if (tab.length > 0) { n = tab.length; }
    // 	else { return null; }
    // 	if (tab[(n - 1)] & hash) { first = tab[(n - 1)] & hash; }
    // 	else { return null; }
    // 	// if (first.hash == hash && // always check first node
    // 	//     ((k = first.key) == key || (key != null && key.equals(k))))
    // //             return first;
    // 	if (first.hash == hash) {
    // 	    if (first.key == key) { return first; }
    // 	    else if (key && key.equals(k)) { return first; }
    // 	}
    // //  if ((e = first.next) != null) {
    // 	if (first.next) { e = first.next; }
    // 	else { return null; }
    //             if (first instanceof TreeNode)
    //                 return ((TreeNode<K,V>)first).getTreeNode(hash, key);
    //             do {
    //                 if (e.hash == hash &&
    //                     ((k = e.key) == key || (key != null && key.equals(k))))
    //                     return e;
    //             } while ((e = e.next) != null);
    //         }
    //     }
    //     return null;
    // }
    final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                   boolean evict) {
        // Node<K,V>[] tab; Node<K,V> p; int n, i;

        // // if ((tab = table) == null || (n = tab.length) == 0)
        // //     n = (tab = resize()).length;
	// if (table) { tab = table; }
	// else if (tab.length == 0) { n = tab.length; }
        // // if ((p = tab[i = (n - 1) & hash]) == null)
        // //     tab[i] = newNode(hash, key, value, null);
	// i = (n - 1) & hash;
	// if (tab[i] == null) {
	//     p = tab[i];
	//     // Calling with null doesn't work. Can't figure out type of last arg.
	//     tab[i] = newNode(hash, key, value, new Node()); 
	//     // tab[i] = newNode(hash, key, value, null); 
	// }
        // else {
        //     Node<K,V> e; K k;
	//     /* Ignoring .equals() */
        // //     if (p.hash == hash &&
        // //         ((k = p.key) == key || (key != null && key.equals(k))))
        // //         e = p;
	//     if ((p.hash == hash && p.key == key) || key != null) { k = p.key; e = p; }
        // //     else if (p instanceof TreeNode)
        // //         e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        // //     else {
        // //         for (int binCount = 0; ; ++binCount) {
        // //             if ((e = p.next) == null) {
        //     else {
	// 	// if ((e = p.next) == null) {
	// 	//     p.next = newNode(hash, key, value, null);
	// 	//     if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
	// 	//         treeifyBin(tab, hash);
	// 	//         break;
	// 	// }
        //         for (int binCount = 0; ; ++binCount) {
	// 	    if (p.next == null) {
	// 		e = p.next;
	// 		p.next = newNode(hash, key, value, new Node());
	// 		// if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
	// 		//     treeifyBin(tab, hash);
	// 	        break;
	// 	    }
        //             // if (e.hash == hash &&
	// 	    //    ((k = e.key) == key || (key != null && key.equals(k))))
	// 	    //       break;
	// 	    // p = e;
        //             if ((e.hash == hash && e.key == key) || key != null) {
	// 		k = e.key;
	// 		break;
	// 	    }
        //             p = e;
        //         }
	//     }
	//     if (e != null) { // existing mapping for key
        //         V oldValue = e.value;
        //         if (!onlyIfAbsent || oldValue == null)
        //             e.value = value;
        //         // afterNodeAccess(e);
        //         return oldValue;
        //     }
        // }
        // ++modCount;
        // // if (++size > threshold)
        //     // resize();
        // // afterNodeInsertion(evict);
        return null;
    }

    // Create a regular (non-tree) node
    Node<K,V> newNode(int hash, K key, V value, Node<K,V> next) {
        return new Node<>(hash, key, value, next);
    }

    class Node<K,V> implements Map.Entry<K,V> {
    	final int hash;
    	final K key;
    	V value;
    	Node<K,V> next;
	
    	Node(int hash, K key, V value, Node<K,V> next) {
    	    this.hash = hash;
    	    this.key = key;
    	    this.value = value;
    	    this.next = next;
    	}

	public boolean equals(Object obj) {
	    return true;
	}
    }
    
    // static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
    class TreeNode<K,V> {
        TreeNode<K,V> parent;  // red-black tree links
        TreeNode<K,V> left;
        TreeNode<K,V> right;
        TreeNode<K,V> prev;    // needed to unlink next upon deletion
        boolean red;
        // TreeNode(int hash, K key, V val, Node<K,V> next) {
        //     super(hash, key, val, next);
        // }
    }
}

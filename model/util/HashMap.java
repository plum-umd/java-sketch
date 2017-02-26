public class HashMap<K,V> extends Object {

    final int MAXIMUM_CAPACITY = 1 << 30;
    final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
    final float DEFAULT_LOAD_FACTOR = 0.75f;

    int threshold;
    // changing numPairs to "size" causes problems
    int numPairs;

    final float loadFactor;

    // class Node<K,V> {
    //     final int hash;
    //     final K key;
    //     V value;
    //     Node<K,V> next;

    //     Node(int hash, K key, V value, Node<K,V> next) {
    //         this.hash = hash;
    //         this.key = key;
    //         this.value = value;
    //         this.next = next;
    //     }

    //     public final K getKey()        { return key; }
    //     public final V getValue()      { return value; }
    //     public final String toString() { return key + "=" + value; }

    //     public final int hashCode() {
    //         return Objects.hashCode(key) ^ Objects.hashCode(value);
    //     }

    //     public final V setValue(V newValue) {
    //         V oldValue = value;
    //         value = newValue;
    //         return oldValue;
    //     }

    //     public final boolean equals(Object o) {
    //         if (o == this)
    //             return true;
    //         if (o instanceof Map.Entry) {
    //             Map.Entry<?,?> e = (Map.Entry<?,?>)o;
    //             if (Objects.equals(key, e.getKey()) &&
    //                 Objects.equals(value, e.getValue()))
    //                 return true;
    //         }
    //         return false;
    //     }
    // }

    public HashMap() {
        this.loadFactor = DEFAULT_LOAD_FACTOR;
	this.threshold = DEFAULT_INITIAL_CAPACITY;
	this.numPairs = 0;
    }

    public int size() {
        return numPairs;
    }

    public boolean isEmpty() {
        return numPairs == 0;
    }

    public boolean containsKey(Object key) {
        return getNode(hash(key), key) != null;
    }

    public boolean containsValue(Object value) {
	return false;
    }
    
    // final Node<K,V> getNode(int hash, Object key) {
    // 	Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    // 	if ((tab = table) != null && (n = tab.length) > 0 &&
    //         (first = tab[(n - 1) & hash]) != null) {
    //         if (first.hash == hash && // always check first node
    //             ((k = first.key) == key || (key != null && key.equals(k))))
    //             return first;
    //         if ((e = first.next) != null) {
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


}

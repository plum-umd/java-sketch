// class HashMap_Node<K,V> extends Object implements Map.Entry<K,V>{
//     final int hash;
    // final K key;
    // V value;
    // Node<K,V> next;
    
    // Node(int hash, K key, V value, Node<K,V> next) {
    // 	this.hash = hash;
    // 	this.key = key;
    // 	this.value = value;
    // 	this.next = next;
    // }
    
    // public final K getKey()        { return key; }
    // public final V getValue()      { return value; }
    // //public final String toString() { return key + "=" + value; }
    
    // public final int hashCode() {
    // 	return Objects.hashCode(key) ^ Objects.hashCode(value);
    // }
    
    // public final V setValue(V newValue) {
    // 	V oldValue = value;
    // 	value = newValue;
    // 	return oldValue;
    // }
    
    // public final boolean equals(Object o) {
    // 	if (o == this)
    // 	    return true;
    // 	// SUB-INTERFACE DOESN'T COMPILE
    // 	// if (o instanceof Map.Entry) {
    // 	//     Map.Entry<?,?> e = (Map.Entry<?,?>)o;
    // 	// if (o instanceof Map_Entry) {
    // 	//     Map_Entry<K,V> e = (Map_Entry<K,V>)o;
    // 	//     if (Objects.equals(key, e.getKey()) &&
    // 	//     	Objects.equals(value, e.getValue()))
    // 	//     	return true;
    // 	// }
    // 	// return false;
    // }
// }


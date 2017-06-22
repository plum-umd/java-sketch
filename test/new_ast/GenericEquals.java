class GenericEquals<K> {
    public static void main(String[] args) {
	HMap<Object, Object> h = new HMap<>();
	Integer i = new Integer(5);
	System.out.println(h.test(i));
    }
}

class Node<K, V> {
    int v;
    Node(int v) { this.v = v; }
}
class HMap<K, V> {
    boolean test(K k) {
	Node<K, V> d = new Node<>(5);
	return d.equals(k);
    }
}

package java.util;

public interface Map<K,V> {
    public void clear();
    public boolean containsKey(K key);
    public V get(K key);
    public V put(K key, V value);
    public V replace(K key, V value);
    
    interface Entry<K,V> {
    	public boolean equals(Object o);
    	// public <K> K getKey();
    	// public <V> V getValue();
    	// public int hashCode();
    	// public <V> V setValue(V value);
    }
}

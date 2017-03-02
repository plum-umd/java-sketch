package java.util;

public interface Map<K,V> {
    public void clear();
    public boolean containsKey(Object key);
    public Object get(Object key);
    public void put(Object key, Object value);
    
    interface Entry<K,V> {
    	public boolean equals(Object o);
    	public <K> K getKey();
    	public <V> V getValue();
    	public int hashCode();
    	public <V> V setValue(V value);
    }
}

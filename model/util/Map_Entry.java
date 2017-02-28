public interface Map_Entry<K,V> {
    public boolean equals(Object o);
    public <K> K getKey();
    public <V> V getValue();
    public int hashCode();
    public <V> V setValue(V value);
}

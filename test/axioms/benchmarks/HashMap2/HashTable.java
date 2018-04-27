package Interfaing;

public interface HashTable<K, V> {
	// put key­value pair into the table
	public void put(K key, V value);

	// get value paired with key, return null if
	// hash don't contain key
	public V get(K key);

	// remove key (and its value) from table
	public void delete(K key);

	// return true if there is a value paired with key
	// and false otherwise.
	public boolean contains(K key);

	// return true if the table is empty.
	public boolean isEmpty();

	// return size of the table.
	public int size();

	// all keys in the table
	Iterable<K> keys();

}
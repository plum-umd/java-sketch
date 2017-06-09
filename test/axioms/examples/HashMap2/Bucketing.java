// run with:
// ./jsk.sh test/axioms/examples/HashMap1/test.java test/axioms/examples/HashMap1/Bucketing.java test/axioms/examples/HashMap1/HashTable.java test/axioms/examples/HashMap1/Pair.java model/lang/ model/util/

package HashingTechnique;

import java.util.ArrayList;

import Interfaing.HashTable;

public class Bucketing<K, V> implements HashTable<K, V> {

	// private Pair<K, V> bucketHash[];
	private Pair<K, V>[] bucketHash;
	private ArrayList<Pair	<K, V>> overflow;
	// private ArrayList<K, V> overflow;
	// private int sizeBucket[];
	private int[] sizeBucket;	
	private int numberOfElements;
	private int index, integerkey;
	private int size;
	private int mod, numberOfSlots;
	private ArrayList<K> ilterator;
	double rehash;

	// mod 10
	// 10 bucket
	public Bucketing() {
		size = 100;
		mod = 10;
		numberOfSlots = 10; // 10;
		bucketHash = new Pair<K,V>[size];
		overflow = new ArrayList<Pair <K,V>>();
		sizeBucket = new int[10];
		numberOfElements = 0;
	}

	public int sizeOfArray() {
		return size;
	}

	public void rehashng() {

		ArrayList<Pair <K, V>> temp1 = new ArrayList();

		for (int i = 0; i < 10; i++) {
			for (int j = 0; j < sizeBucket[i]; j++) {

				int index = i * numberOfSlots + j;
				temp1.add(new Pair(bucketHash[index].key,
						bucketHash[index].value));
			}
		}
		for (int i = 0; i < overflow.size(); i++) {
			Pair<K,V> tmp = overflow.get(i);
			// temp1.add(overflow.get(i));
			temp1.add(tmp);			
		}

		size *= 4;
		numberOfSlots *= 2;
		mod *= 2;
		bucketHash = new Pair[size];
		sizeBucket = new int[mod];
		numberOfElements = 0;

		for (int i = 0; i < temp1.size(); i++) {
			Pair<K,V> tmp = temp1.get(i);
			K key = tmp.key;
			V val = tmp.value;			
			// put(temp1.get(i).key, temp1.get(i).value);
			put(key, val);
		}

	}

	@Override
	public void put(K key, V value) {
		delete(key);
		// integerkey = Math.abs(key.hashCode() % mod);
		integerkey = key.hashCode() % mod;
		if (integerkey < 0) { 
			integerkey *= -1;
		}
		// // check if there is a place in buckting array or not
		if (sizeBucket[integerkey] != numberOfSlots) {
			int index = numberOfSlots * integerkey + sizeBucket[integerkey];
			bucketHash[index] = new Pair(key, value);
			sizeBucket[integerkey]++;

		} else {
			overflow.add(new Pair(key, value));
		}
		numberOfElements++;
		rehash = (double) numberOfElements / (double) size;
		if (rehash > 0.75)
			rehashng();

	}

	// generator public int chooseInt(int[] localInts) {
	// 	int s0 = sizeBucket[0];
	// 	int s1 = sizeBucket[1];
	// 	int s2 = sizeBucket[2];
	// 	int s3 = sizeBucket[3];
	// 	int s4 = sizeBucket[4];
	// 	int s5 = sizeBucket[5];
	// 	int s6 = sizeBucket[6];
	// 	int s7 = sizeBucket[7];
	// 	int s8 = sizeBucket[8];
	// 	int s9 = sizeBucket[9];		
						
	// 	// int sizeBucketElement = {| s0,s1,s2,s3,s4,s5,s6,s7,s8,s9 |};
	
	// 	int local = localInts[??];

	// 	return {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, overflow.size(), ?? |};
	// }

	@Override
	public V get(K key) {
		// integerkey = Math.abs(key.hashCode() % mod);
		integerkey = key.hashCode() % mod;
		if (integerkey < 0) { 
			integerkey *= -1;
		}
		index = numberOfSlots * integerkey;

		int s0 = sizeBucket[0];
		int s1 = sizeBucket[1];
		int s2 = sizeBucket[2];
		int s3 = sizeBucket[3];
		int s4 = sizeBucket[4];
		int s5 = sizeBucket[5];
		int s6 = sizeBucket[6];
		int s7 = sizeBucket[7];
		int s8 = sizeBucket[8];
		int s9 = sizeBucket[9];		
		int o_size = overflow.size();
		int rand1 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};
		int rand2 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};
		int rand3 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};
		int rand4 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};
		V val = null;

		for (int i = rand1; i-sizeBucket[integerkey] < rand2; i++) {
		// for (int i = index; i < index + sizeBucket[integerkey]; i++) {
			Pair<K,V> tmp = bucketHash[i];
			K tmp_key = tmp.key;
			// if (bucketHash[i].key.equals(key))
			// 	return bucketHash[i].value;
			boolean bool = tmp_key.equals(key);
			if ({| bool, tmp_key == key |})
			// if (tmp_key.equals(key))
      			    //return bucketHash[i].value;
			    val = bucketHash[i].value;
		}

		if (sizeBucket[integerkey] == numberOfSlots) {
			for (int i = rand3; i < rand4; i++) {
			// for (int i = 0; i < overflow.size(); i++) {
				Pair<K,V> tmp = overflow.get(i);
				K tmp_key = tmp.key;				
				// if (overflow.get(i).key.equals(key))
				// 	return overflow.get(i).value;
				boolean bool = tmp_key.equals(key);
				if ({| bool, tmp_key == key |})				
				// if (tmp_key.equals(key))
					//return tmp.value;
					val = tmp.value;
			}
		}
		return val;
	}

	@Override
	public void delete(K key) {
		// integerkey = Math.abs(key.hashCode() % mod);
		integerkey = key.hashCode() % mod;
		if (integerkey < 0) { 
			integerkey *= -1;
		}
		index = numberOfSlots * integerkey;
		boolean flag = false;

		int s0 = sizeBucket[0];
		int s1 = sizeBucket[1];
		int s2 = sizeBucket[2];
		int s3 = sizeBucket[3];
		int s4 = sizeBucket[4];
		int s5 = sizeBucket[5];
		int s6 = sizeBucket[6];
		int s7 = sizeBucket[7];
		int s8 = sizeBucket[8];
		int s9 = sizeBucket[9];		
		int o_size = overflow.size();
		int rand1 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};
		int rand2 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};
		int rand3 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};
		int rand4 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, integerkey, o_size, ?? |};

		// for (int i = rand1; i-sizeBucket[integerkey] < rand2; i++) {
		for (int i = index; i < index + sizeBucket[integerkey]; i++) {
		    Pair<K,V> tmp = bucketHash[i];
    		    boolean bool = tmp.key.equals(key);
		    if ({| tmp.key == key, bool |}) {
		    // if (bucketHash[i].key.equals(key)) {
			flag = true;
		    } else if (flag) {
			bucketHash[i - 1] = new Pair(bucketHash[i].key,
						     bucketHash[i].value);
			
		    }
		}
		if (flag) {
			numberOfElements--;
			sizeBucket[integerkey]--;
		} 
		else if (sizeBucket[integerkey] == numberOfSlots) {
			// for (int i = rand3; i < rand4; i++) {
			for (int i = 0; i < overflow.size(); i++) {
				Pair<K,V> tmp = overflow.get(i);
				K tmp_key = tmp.key;
				// if (overflow.get(i).key.equals(key)) {
				// 	overflow.remove(i);
				// 	numberOfElements--;
				// 	break;
				// }
				boolean bool = tmp_key.equals(key);
				if ({| bool, tmp_key == key |}) {
				// if (tmp_key.equals(key)) {
				    overflow.remove(i);
				    numberOfElements--;
				    break;
				}
			}
		}

	}

	@Override
	public boolean contains(K key) {
		V check = get(key);
		if (check == null)
			return false;
		return true;
	}

	@Override
	public boolean isEmpty() {
		if (numberOfElements == 0)
			return true;
		return false;
	}

	@Override
	// public int size() {	
	public int size2() {

		return numberOfElements;
	}

	@Override
	public Iterable<K> keys() {
		ilterator = new ArrayList();
		for (int i = 0; i < 10; i++) {
			for (int j = 0; j < sizeBucket[i]; j++) {
				int index = i * numberOfSlots + j;
				ilterator.add(bucketHash[index].key);

			}
		}
		for (int i = 0; i < overflow.size(); i++) {
			// ilterator.add(overflow.get(i).key);
			Pair<K,V> tmp = overflow.get(i);
			ilterator.add(tmp.key);			

		}
		return ilterator;
	}

}

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
		size = 10;
		mod = 2;
		numberOfSlots = 2; // 10;
		bucketHash = new Pair<K,V>[size];
		overflow = new ArrayList<Pair <K,V>>();
		sizeBucket = new int[2];
		numberOfElements = 0;
	}

	public int sizeOfArray() {
		return size;
	}

	public void rehashng() {

		ArrayList<Pair <K, V>> temp1 = new ArrayList();

		int i_gen1 = getInt2();
		int i_gen2 = getInt2();
		int i_gen3 = getInt2();		
		
		// for (int i = ??; i < ??; i++) {
		// 	for (int j = ??; j < i_gen1; j++) {
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < sizeBucket[i]; j++) {

				int index = i * numberOfSlots + j;
				temp1.add(new Pair(bucketHash[index].key,
						   bucketHash[index].value));
			}
		}
		// for (int i = ??; i < i_gen2; i++) {
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

		// for (int i = ??; i < i_gen3; i++) {
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

		int i_gen1 = getInt2();
		int i_gen2 = getInt2();		

		if (integerkey < 0) { 
			integerkey *= -1;
		}
		// // check if there is a place in buckting array or not
		if (sizeBucket[integerkey] != numberOfSlots) {
		// if (i_gen1 != i_gen2) {
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

    generator public int getInt2() {
	    int o_size = overflow.size();
	    int s0 = sizeBucket[0];
	    int s1 = sizeBucket[1];
	    int si = sizeBucket[integerkey];
	    // int a = {|-3, -2, -1, 0, 1, 2, 3 |};
	    // int b = {|-3, -2, -1, 0, 1, 2, 3 |};	    
	    // int c = {|-3, -2, -1, 0, 1, 2, 3 |};	    
	    int i1 = {| numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, si, o_size |};
	    return i1;
    }
    
        // generator public int getInt() {
	//     int o_size = overflow.size();
	//     int s0 = sizeBucket[0];
	//     int s1 = sizeBucket[1];
	//     int a = {|-3, -2, -1, 0, 1, 2, 3 |};
	//     int b = {|-3, -2, -1, 0, 1, 2, 3 |};	    
	//     int c = {|-3, -2, -1, 0, 1, 2, 3 |};	    
	//     int i1 = {| numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, o_size |};
	//     int i2 = {| numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, o_size |};
	//     // return ??*i1+??*i2+??;
	//     return a*i1+b*i2+c;
        // }
    
	@Override
	public V get(K key) {
		// integerkey = Math.abs(key.hashCode() % mod);
		integerkey = key.hashCode() % mod;
		if (integerkey < 0) { 
			integerkey *= -1;
		}
		index = numberOfSlots * integerkey;

		// int s0 = sizeBucket[0];
		// int s1 = sizeBucket[1];
		// int o_size = overflow.size();
		// int rand1 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		// int rand2 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		// int rand3 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		// int rand4 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		int i_gen1 = getInt2();
		int i_gen2 = getInt2();
		// int i_gen3 = getInt2();
		int i_gen4 = getInt2();		
		int i_gen5 = getInt2();		
		int i_gen6 = getInt2();		
		V val = null;

		for (int i = i_gen1; i < i_gen1+i_gen2; i++) {
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

		// if (i_gen5 == i_gen6) {
		if (sizeBucket[integerkey] == numberOfSlots) {
			for (int i = ??; i < i_gen4; i++) {
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

		// int s0 = sizeBucket[0];
		// int s1 = sizeBucket[1];
		// int o_size = overflow.size();
		// int rand1 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		// int rand2 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		// int rand3 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		// int rand4 = {|numberOfElements, index, integerkey, size, mod, numberOfSlots, s0, s1, integerkey, o_size, ?? |};
		int i_gen1 = getInt2();
		int i_gen2 = getInt2();
		// int i_gen3 = getInt2();
		int i_gen4 = getInt2();		
		int i_gen5 = getInt2();		
		int i_gen6 = getInt2();		
		
		for (int i = i_gen1; i < i_gen1+i_gen2; i++) {
		// for (int i = index; i < index + sizeBucket[integerkey]; i++) {
		    Pair<K,V> tmp = bucketHash[i];
    		    boolean bool = tmp.key.equals(key);
		    // if ({| tmp.key == key, bool |}) {
		    if (bucketHash[i].key.equals(key)) {
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
		// else if (i_gen5 == i_gen6) {
		else if (sizeBucket[integerkey] == numberOfSlots) {
			// for (int i = ??; i < i_gen4; i++) {
			for (int i = 0; i < overflow.size(); i++) {
				Pair<K,V> tmp = overflow.get(i);
				K tmp_key = tmp.key;
				// if (overflow.get(i).key.equals(key)) {
				// 	overflow.remove(i);
				// 	numberOfElements--;
				// 	break;
				// }
				boolean bool = tmp_key.equals(key);
				// if ({| bool, tmp_key == key |}) {
				if (tmp_key.equals(key)) {
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
		for (int i = 0; i < 2; i++) {
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

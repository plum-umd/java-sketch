public class simple_hash {

	int size;
	int numElements;

	public simple_hash() {
		size = 10;
		numElements = 0;
	}

	public void rehashng() {
		ArrayList<Integer> temp1 = new ArrayList();

		size *= 10;

		for (int i = 0; i < temp1.size(); i++) {		
			put(0, 0);
		}

	}

	public void put(int i, int j) {
		numElements++;
		double rehash = (double) numElements / (double) size;
		if (rehash > 0.75) 
			rehashng();
	}
}
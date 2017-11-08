public class simple_test {

	harness public static boolean test() {
		boolean ok = true;
		simple_hash ht1 = new simple_hash();
		String s = "";
		int j = 4;
		Integer i2 = new Integer(0);
		for (int i=0;i<2;i++) {
			// String s = String.valueOf(i*100);
			ht1.put(i, j);
		}

		// int j = 4;
		// ht1.put(0,j);
		// j = 4;
		// ht1.put(1,j);

		return ok;		
	}


}
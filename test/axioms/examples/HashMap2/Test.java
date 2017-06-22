import HashingTechnique.Bucketing;
import HashingTechnique.DoubleHashing;
import HashingTechnique.LinearProbing;
import HashingTechnique.PseudoRandomProbing;
import HashingTechnique.QuadraticProbing;
import HashingTechnique.SeparateChaining;





public class Test {
	
	// public static boolean testChaining() {
	// 	boolean ok = true;
	// 	SeparateChaining<Integer, String> ht1 = new SeparateChaining<>();
	// 	for (int i=0;i<100;i++) {
	// 		String s = String.valueOf(i*100);
	// 		ht1.put(i*10, s);
	// 	}
	// //	System.out.println(ht1.co() + " collisions occurred in test 1.");
	// 	System.out.println("The size of the hashtable is " + ht1.size());
	// 	for (int i=0;i<100;i++) {
	// 		String s = String.valueOf(i*100);
	// 		if (!ht1.get(i*10).equals(s)) {
	// 			ok = false;
	// 		}
	// 	}
	// 	SeparateChaining<Integer, String> ht2 = new SeparateChaining<>();
	// 	for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		ht2.put(i, s);
	// 	}
	// //	System.out.println(ht2.getCollesions() + " collisions occurred in test 2.");
	// 	System.out.println("The size of the hashtable is " + ht2.size());
	// 	for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		if (!ht2.get(i).equals(s)) {
	// 			ok = false;
	// 		}
	// 	}
	// 	return ok;
	// }
	
	public static boolean testBucketing() {
		boolean ok = true;
		Bucketing<Integer, String> ht1 = new Bucketing<Integer, String>();

		Integer i0 = new Integer(2);
		Integer i1 = new Integer(4);
		Integer i2 = new Integer(6);
		Integer i3 = new Integer(8);		
		Integer i4 = new Integer(10);
		Integer i5 = new Integer(1);		
		Integer i6 = new Integer(3);		
		Integer i7 = new Integer(5);		

		String s0 = "0";
		String s1 = "1";
		String s2 = "2";
		String s3 = "3";
		String s4 = "4";
		String s5 = "5";		
		String s6 = "6";		
		String s7 = "7";		
		String s4_2= "4_2";		

		ht1.put(i0, s0);
		String gs0 = ht1.get(i0);
		Assert.assertTrue(gs0.equals(s0));

		ht1.put(i1, s1);
		String gs1 = ht1.get(i1);		
		Assert.assertTrue(gs1.equals(s1));
		
		ht1.put(i2, s2);
		String gs2 = ht1.get(i2);		
		Assert.assertTrue(gs2.equals(s2));

		ht1.put(i3, s3);		
		String gs3 = ht1.get(i3);
		Assert.assertTrue(gs3.equals(s3));
		
		ht1.put(i4, s4);
		String gs4 = ht1.get(i4);		
		Assert.assertTrue(gs4.equals(s4));		

		ht1.put(i4, s4_2);		
		gs4 = ht1.get(i4);
		Assert.assertTrue(gs4.equals(s4_2));

		ht1.put(i5, s5);
		ht1.put(i6, s6);
		// ht1.put(i7, s7);

		gs0 = ht1.get(i0);
		Assert.assertTrue(gs0.equals(s0));
		gs1 = ht1.get(i1);
		Assert.assertTrue(gs1.equals(s1));
		gs2 = ht1.get(i2);
		Assert.assertTrue(gs2.equals(s2));
		gs3 = ht1.get(i3);
		Assert.assertTrue(gs3.equals(s3));
		gs4 = ht1.get(i4);
		Assert.assertTrue(gs4.equals(s4_2));
		String gs5 = ht1.get(i5);
		Assert.assertTrue(gs5.equals(s5));
		String gs6 = ht1.get(i6);
		Assert.assertTrue(gs6.equals(s6));
		// String gs7 = ht1.get(i7);
		// Assert.assertTrue(gs7.equals(s7));
		
		// for (int i=0;i<10;i++) {
		// 	// String s = String.valueOf(i*100);
		// 	String s = "";
		// 	Integer i2 = new Integer(i*10);
		// 	ht1.put(i2, s);
		// }
	// //	System.out.println(ht1.() + " collisions occurred in test 1.");
	// 	System.out.println("The size of the hashtable is " + ht1.size());
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		if (!ht1.get(i*10).equals(s)) {
	// 			ok = false;
	// 		}
	// 	}
	// 	Bucketing<Integer, String> ht2 = new Bucketing<>();
 // 		for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		ht2.put(i, s);
	// 	}
	// 	ht2.delete(10);
	// //	System.out.println(ht2.getCollesions() + " collisions occurred in test 2.");
	// 	System.out.println("The size of the hashtable is " + ht2.size());
	// 	for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		if (!ht2.contains(i) && i != 10)
	// 			ok = false;
	// 		if (i != 10) {
	// 			if (!ht2.get(i).equals(s)) {
	// 				ok = false;
	// 			}
	// 		}
	// 	}
		return ok;
	}
	
	// public static boolean testLinear() {
	// 	boolean ok = true;
	// 	LinearProbing<Integer, String> ht1 = new LinearProbing<>();
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		ht1.put(i*10, s);
	// 	}
	// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
	// 	System.out.println("The size of the hashtable is " + ht1.size());
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		if (!ht1.get(i*10).equals(s)) {
	// 			ok = false;
	// 		}
	// 	}
	// 	LinearProbing<Integer, String> ht2 = new LinearProbing<>();
 // 		for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		ht2.put(i, s);
	// 	}
	// 	ht2.delete(10);
	// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
	// 	System.out.println("The size of the hashtable is " + ht2.size());
	// 	for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		if (!ht2.contains(i) && i != 10)
	// 			ok = false;
	// 		if (i != 10) {
	// 			if (!ht2.get(i).equals(s)) {
	// 				ok = false;
	// 			}
	// 		}
	// 	}
	// 	return ok;
	// }
	
	// public static boolean testQuadratic() {
	// 	boolean ok = true;
	// 	QuadraticProbing<Integer, String> ht1 = new QuadraticProbing<>();
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		ht1.put(i*10, s);
	// 	}
	// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
	// 	System.out.println("The size of the hashtable is " + ht1.size());
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		if (!ht1.get(i*10).equals(s)) {
	// 			ok = false;
	// 		}
	// 	}
	// 	QuadraticProbing<Integer, String> ht2 = new QuadraticProbing<>();
 // 		for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		ht2.put(i, s);
	// 	}
	// 	ht2.delete(10);
	// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
	// 	System.out.println("The size of the hashtable is " + ht2.size());
	// 	for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		if (!ht2.contains(i) && i != 10)
	// 			ok = false;
	// 		if (i != 10) {
	// 			if (!ht2.get(i).equals(s)) {
	// 				ok = false;
	// 			}
	// 		}
	// 	}
	// 	return ok;
	// }

	// public static boolean testRandom() {
	// 	boolean ok = true;
	// 	PseudoRandomProbing<Integer, String> ht1 = new PseudoRandomProbing<>();
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		ht1.put(i*10, s);
	// 	}
	// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
	// 	System.out.println("The size of the hashtable is " + ht1.size());
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		if (!ht1.get(i*10).equals(s)) {
	// 			ok = false;
	// 		}
	// 	}
	// 	PseudoRandomProbing<Integer, String> ht2 = new PseudoRandomProbing<>();
 // 		for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		ht2.put(i, s);
	// 	}
	// 	ht2.delete(10);
	// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
	// 	System.out.println("The size of the hashtable is " + ht2.size());
	// 	for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		if (!ht2.contains(i) && i != 10)
	// 			ok = false;
	// 		if (i != 10) {
	// 			if (!ht2.get(i).equals(s)) {
	// 				ok = false;
	// 			}
	// 		}
	// 	}
	// 	return ok;
	// }
	
	// public static boolean testDouble() {
	// 	boolean ok = true;
	// 	DoubleHashing<Integer, String> ht1 = new DoubleHashing<>();
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		ht1.put(i*10, s);
	// 	}
	// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
	// 	System.out.println("The size of the hashtable is " + ht1.size());
	// 	for (int i=0;i<10;i++) {
	// 		String s = String.valueOf(i*100);
	// 		if (!ht1.get(i*10).equals(s)) {
	// 			ok = false;
	// 		}
	// 	}
	// 	DoubleHashing<Integer, String> ht2 = new DoubleHashing<>();
 // 		for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		ht2.put(i, s);
	// 	}
	// 	ht2.delete(10);
	// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
	// 	System.out.println("The size of the hashtable is " + ht2.size());
	// 	for (int i=0;i<26;i++) {
	// 		String s = String.valueOf('A' + i);
	// 		if (!ht2.contains(i) && i != 10)
	// 			ok = false;
	// 		if (i != 10) {
	// 			if (!ht2.get(i).equals(s)) {
	// 				ok = false;
	// 			}
	// 		}
	// 	}
	// 	return ok;
	// }
	
	harness public static void main() {
		// System.out.println("Testing chaining ...");
		// if (testChaining())
		// 	System.out.println("Test successful!");
		// else
		// 	System.err.println("Test failed!");
		// System.out.println("Testing bucketing ...");
		// if (testBucketing())
		// 	System.out.println("Test successful!");
		// else
		// 	System.err.println("Test failed!");
		// System.out.println("Testing linear probing ...");
		// if (testLinear())
		// 	System.out.println("Test successful!");
		// else
		// 	System.err.println("Test failed!");
		// System.out.println("Testing quadratic probing ...");
		// if (testQuadratic())
		// 	System.out.println("Test successful!");
		// else
		// 	System.err.println("Test failed!");
		// System.out.println("Testing psuedo-random probing ...");
		// if (testRandom())
		// 	System.out.println("Test successful!");
		// else
		// 	System.err.println("Test failed!");
		// System.out.println("Testing double hashing ...");
		// if (testDouble())
		// 	System.out.println("Test successful!");
		// else
		// 	System.err.println("Test failed!");
		assert testBucketing();
	}

}

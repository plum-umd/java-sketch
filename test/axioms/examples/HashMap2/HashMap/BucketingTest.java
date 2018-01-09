// This code is from https://github.com/anthonynsimon/java-ds-algorithms

import org.junit.Assert;

public class BucketingTest {
    private Bucketing<Object, Object> classUnderTest;

    harness void mn() {
    // harness void mn(int x, int y, int z) {      
	// assume x != y && x != z && y != z;

	int x = 1;
	int y = 2;
	int z = 3;
	
	Integer xx = new Integer(x);
	Integer yy = new Integer(y);
	Integer zz = new Integer(z);

	setUp();
	testClear(xx, yy);
	testGetEmpty();
	testPutAndGet(xx, yy, zz);
	// testReplacing(xx, yy, zz);
	// testKeys(xx, yy);
	// testValues(xx, yy);
	// testContainsValue(xx, yy);
	// testContainsKey(xx, yy);
	// testRemoveNonExistent(xx, yy);
	// testRemove(xx, yy);
	// if (x >= INITIAL_SIZE && x < 0) { testSize(x, y); }

	/* Something is wrong with expanding. Maybe hash function? */
	// testEnsureCapacity(vv, ww, xx, yy, zz);
    }
    public void setUp() {
        classUnderTest = new Bucketing<>();
    }

    public void testClear(Integer x, Integer y) {
	// classUnderTest.clear();

        classUnderTest.put(x, y);
        classUnderTest.put(y, x);
        Assert.assertTrue(classUnderTest.size() > 0);
        
	classUnderTest.clear();
	Assert.assertFalse(classUnderTest.size() > 0);
    }

    public void testGetEmpty() {
        classUnderTest.clear();
        Assert.assertNull(classUnderTest.get(null));
    }

    public void testPutAndGet(Integer x, Integer y, Integer z) {
        classUnderTest.clear();

        classUnderTest.put(x, y);
        classUnderTest.put(y, x);
        classUnderTest.put(z, x);
        Assert.assertEquals(classUnderTest.get(x), y);
        Assert.assertEquals(classUnderTest.get(y), x);
        Assert.assertEquals(classUnderTest.get(z), x);

	int i2 = x.intValue()+1;
    	Integer i = new Integer(i2);
        classUnderTest.put(i, y);
        Assert.assertEquals(classUnderTest.get(i), y);
    }

    public void testReplacing(Integer x, Integer y, Integer z) {
        // classUnderTest.clear();
    	// Integer i = new Integer(x.intValue()+INITIAL_SIZE);
        // classUnderTest.put(i, z);
        // Assert.assertEquals(classUnderTest.get(i), z);

        // classUnderTest.put(x, y);
        // Assert.assertEquals(classUnderTest.get(x), y);

        // int size = classUnderTest.size();

        // classUnderTest.put(x, z);
        // Assert.assertEquals(classUnderTest.get(x), z);

    	// classUnderTest.put(i, z);
        // Assert.assertEquals(classUnderTest.get(i), z);

        // Assert.assertEquals(classUnderTest.size(), size);

    }

    public void testKeys(Integer x, Integer y) {
        // classUnderTest.clear();

        // classUnderTest.put(x, y);
    	// Object k = classUnderTest.keys()[0];
        // Assert.assertTrue(k.equals(x));
    	// // TODO: array access from method call as argument to assertTrue
        // // Assert.assertEquals(classUnderTest.keys()[0], k);

    	// Object[] keys = classUnderTest.keys();
        // Assert.assertTrue(keys.length == 1);
     }

    // @Test
    public void testValues(Integer x, Integer y) {
        // classUnderTest.clear();
    	// for (int i = 0; i < INITIAL_SIZE; i++) {
    	//     Integer xx = new Integer(x.intValue() + i);
    	//     Integer yy = new Integer(y.intValue() + i);
    	//     classUnderTest.put(xx, yy);
    	// }

    	// Object[] k = classUnderTest.values();
        // // Assert.assertTrue(k.equals(y));
    	// // TODO: array access from method call as argument to assertTrue
        // // Assert.assertEquals(classUnderTest.values()[0], k);
    }

    // TODO: why the heck is this so slow?! containsValue()????
    public void testContainsValue(Integer x, Integer y) {
        // classUnderTest.clear();

        // Assert.assertFalse(classUnderTest.containsValue(y));
        // classUnderTest.put(x, y);
    	// Assert.assertTrue(classUnderTest.containsValue(y));
    }

    public void testContainsKey(Integer x, Integer y) {
        // classUnderTest.clear();

        // Assert.assertFalse(classUnderTest.containsKey(x));
        // classUnderTest.put(x, y);
    	// Assert.assertTrue(classUnderTest.containsKey(x));
    }

    public void testSize(int x, int y) {
    	// assume x >= INITIAL_SIZE && x < 0;
        // classUnderTest.clear();

    	// // had to reduce loop size from original (2048)
    	// for (int i = 0; i < INITIAL_SIZE; i++) { classUnderTest.put(new Integer(i), null); }
        // Assert.assertEquals(classUnderTest.size(), INITIAL_SIZE);
        // classUnderTest.put(new Integer(x), new Integer(y));
        // Assert.assertEquals(classUnderTest.size(), 17);
    }

    public void testRemoveNonExistent(Integer x, Integer y) {
        // classUnderTest.clear();

        // classUnderTest.put(x, y);
        // int size = classUnderTest.size();
        // classUnderTest.remove(y);
        // Assert.assertEquals(classUnderTest.size(), size);
    }

    public void testRemove(Integer x, Integer y) {
        // classUnderTest.clear();

        // int size = classUnderTest.size();
        // classUnderTest.put(x, y);

        // Assert.assertEquals(classUnderTest.get(x), y);
        // Assert.assertEquals(classUnderTest.size(), size + 1);

        // classUnderTest.remove(x);
        // Assert.assertNull(classUnderTest.get(x));
    }

    // Doesn't exist in HashMap2
    // public void testEnsureCapacity(Integer v, Integer w, Integer x, Integer y, Integer z) {
    // 	classUnderTest.clear();

    //     classUnderTest.put(v, w);
    //     classUnderTest.put(w, x);
    //     classUnderTest.put(x, y);
    //     classUnderTest.put(y, z);
    //     classUnderTest.put(z, v);
	
    //     Assert.assertEquals(classUnderTest.get(v), w);
    //     Assert.assertEquals(classUnderTest.get(w), x);
    //     Assert.assertEquals(classUnderTest.get(x), y);
    //     Assert.assertEquals(classUnderTest.get(y), z);
    //     Assert.assertEquals(classUnderTest.get(z), v);
    // }
}

/*********** ORIGINAL *********/
// import HashingTechnique.Bucketing;
// import HashingTechnique.DoubleHashing;
// import HashingTechnique.LinearProbing;
// import HashingTechnique.PseudoRandomProbing;
// import HashingTechnique.QuadraticProbing;
// import HashingTechnique.SeparateChaining;

// public class test {
//     public static boolean testChaining() {
// 	boolean ok = true;
// 	SeparateChaining<Integer, String> ht1 = new SeparateChaining<>();
// 	for (int i=0;i<100;i++) {
// 	    String s = String.valueOf(i*100);
// 	    ht1.put(i*10, s);
// 	}
// 	//	System.out.println(ht1.co() + " collisions occurred in test 1.");
// 	System.out.println("The size of the hashtable is " + ht1.size());
// 	for (int i=0;i<100;i++) {
// 	    String s = String.valueOf(i*100);
// 	    if (!ht1.get(i*10).equals(s)) {
// 		ok = false;
// 	    }
// 	}
// 	SeparateChaining<Integer, String> ht2 = new SeparateChaining<>();
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    ht2.put(i, s);
// 	}
// 	//	System.out.println(ht2.getCollesions() + " collisions occurred in test 2.");
// 	System.out.println("The size of the hashtable is " + ht2.size());
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    if (!ht2.get(i).equals(s)) {
// 		ok = false;
// 	    }
// 	}
// 	return ok;
//     }
	
//     public static boolean testBucketing() {
// 	boolean ok = true;
// 	Bucketing<Integer, String> ht1 = new Bucketing<>();
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    ht1.put(i*10, s);
// 	}
// 	//	System.out.println(ht1.() + " collisions occurred in test 1.");
// 	System.out.println("The size of the hashtable is " + ht1.size());
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    if (!ht1.get(i*10).equals(s)) {
// 		ok = false;
// 	    }
// 	}
// 	Bucketing<Integer, String> ht2 = new Bucketing<>();
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    ht2.put(i, s);
// 	}
// 	ht2.delete(10);
// 	//	System.out.println(ht2.getCollesions() + " collisions occurred in test 2.");
// 	System.out.println("The size of the hashtable is " + ht2.size());
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    if (!ht2.contains(i) && i != 10)
// 		ok = false;
// 	    if (i != 10) {
// 		if (!ht2.get(i).equals(s)) {
// 		    ok = false;
// 		}
// 	    }
// 	}
// 	return ok;
//     }
	
//     public static boolean testLinear() {
// 	boolean ok = true;
// 	LinearProbing<Integer, String> ht1 = new LinearProbing<>();
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    ht1.put(i*10, s);
// 	}
// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
// 	System.out.println("The size of the hashtable is " + ht1.size());
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    if (!ht1.get(i*10).equals(s)) {
// 		ok = false;
// 	    }
// 	}
// 	LinearProbing<Integer, String> ht2 = new LinearProbing<>();
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    ht2.put(i, s);
// 	}
// 	ht2.delete(10);
// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
// 	System.out.println("The size of the hashtable is " + ht2.size());
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    if (!ht2.contains(i) && i != 10)
// 		ok = false;
// 	    if (i != 10) {
// 		if (!ht2.get(i).equals(s)) {
// 		    ok = false;
// 		}
// 	    }
// 	}
// 	return ok;
//     }
	
//     public static boolean testQuadratic() {
// 	boolean ok = true;
// 	QuadraticProbing<Integer, String> ht1 = new QuadraticProbing<>();
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    ht1.put(i*10, s);
// 	}
// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
// 	System.out.println("The size of the hashtable is " + ht1.size());
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    if (!ht1.get(i*10).equals(s)) {
// 		ok = false;
// 	    }
// 	}
// 	QuadraticProbing<Integer, String> ht2 = new QuadraticProbing<>();
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    ht2.put(i, s);
// 	}
// 	ht2.delete(10);
// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
// 	System.out.println("The size of the hashtable is " + ht2.size());
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    if (!ht2.contains(i) && i != 10)
// 		ok = false;
// 	    if (i != 10) {
// 		if (!ht2.get(i).equals(s)) {
// 		    ok = false;
// 		}
// 	    }
// 	}
// 	return ok;
//     }

//     public static boolean testRandom() {
// 	boolean ok = true;
// 	PseudoRandomProbing<Integer, String> ht1 = new PseudoRandomProbing<>();
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    ht1.put(i*10, s);
// 	}
// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
// 	System.out.println("The size of the hashtable is " + ht1.size());
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    if (!ht1.get(i*10).equals(s)) {
// 		ok = false;
// 	    }
// 	}
// 	PseudoRandomProbing<Integer, String> ht2 = new PseudoRandomProbing<>();
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    ht2.put(i, s);
// 	}
// 	ht2.delete(10);
// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
// 	System.out.println("The size of the hashtable is " + ht2.size());
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    if (!ht2.contains(i) && i != 10)
// 		ok = false;
// 	    if (i != 10) {
// 		if (!ht2.get(i).equals(s)) {
// 		    ok = false;
// 		}
// 	    }
// 	}
// 	return ok;
//     }
	
//     public static boolean testDouble() {
// 	boolean ok = true;
// 	DoubleHashing<Integer, String> ht1 = new DoubleHashing<>();
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    ht1.put(i*10, s);
// 	}
// 	System.out.println(ht1.collis() + " collisions occurred in test 1.");
// 	System.out.println("The size of the hashtable is " + ht1.size());
// 	for (int i=0;i<10;i++) {
// 	    String s = String.valueOf(i*100);
// 	    if (!ht1.get(i*10).equals(s)) {
// 		ok = false;
// 	    }
// 	}
// 	DoubleHashing<Integer, String> ht2 = new DoubleHashing<>();
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    ht2.put(i, s);
// 	}
// 	ht2.delete(10);
// 	System.out.println(ht2.collis() + " collisions occurred in test 2.");
// 	System.out.println("The size of the hashtable is " + ht2.size());
// 	for (int i=0;i<26;i++) {
// 	    String s = String.valueOf('A' + i);
// 	    if (!ht2.contains(i) && i != 10)
// 		ok = false;
// 	    if (i != 10) {
// 		if (!ht2.get(i).equals(s)) {
// 		    ok = false;
// 		}
// 	    }
// 	}
// 	return ok;
//     }
	
//     public static void main(String[] args) {
// 	System.out.println("Testing chaining ...");
// 	if (testChaining())
// 	    System.out.println("Test successful!");
// 	else
// 	    System.err.println("Test failed!");
// 	System.out.println("Testing bucketing ...");
// 	if (testBucketing())
// 	    System.out.println("Test successful!");
// 	else
// 	    System.err.println("Test failed!");
// 	System.out.println("Testing linear probing ...");
// 	if (testLinear())
// 	    System.out.println("Test successful!");
// 	else
// 	    System.err.println("Test failed!");
// 	System.out.println("Testing quadratic probing ...");
// 	if (testQuadratic())
// 	    System.out.println("Test successful!");
// 	else
// 	    System.err.println("Test failed!");
// 	System.out.println("Testing psuedo-random probing ...");
// 	if (testRandom())
// 	    System.out.println("Test successful!");
// 	else
// 	    System.err.println("Test failed!");
// 	System.out.println("Testing double hashing ...");
// 	if (testDouble())
// 	    System.out.println("Test successful!");
// 	else
// 	    System.err.println("Test failed!");
//     }
// }

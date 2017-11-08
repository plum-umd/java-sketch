// This code is from https://github.com/anthonynsimon/java-ds-algorithms

import org.junit.Before;
import org.junit.Test;

import java.util.Random;
import java.util.UUID;

import org.junit.Assert;


public class HashTableTest {
     // static so it will be initialised when translated
    public static final int INITIAL_SIZE = 8;

    private HashTable<Object, Object> classUnderTest;

    // harness void mn(int v, int w, int x, int y, int z) {
    // 	assume v !=w && v != x && v != y && v != z &&
    // 	    w != x && w != y && w != z &&
    // 	    x != y && x != z &&
    // 	    y != z;
	// Integer vv = new Integer(v);
	// Integer ww = new Integer(w);
    harness void mn(int x, int y, int z) {
	assume x != y && x != z && y != z;
	    
	Integer xx = new Integer(x);
	Integer yy = new Integer(y);
	Integer zz = new Integer(z);
	setUp();
	testClear(xx, yy);
	// testPutAndGet(xx, yy, zz);
	// testGetEmpty();
	// testReplacing(xx, yy, zz);
	// testKeys(xx, yy);
	// testValues(xx, yy);
	// testContainsValue(xx, yy);
	// testContainsKey(xx, yy);
	// testRemoveNonExistent(xx, yy);
	// testRemove(xx, yy);
	// if (x >= INITIAL_SIZE && x < 0) { testSize(x, y); }

	// testEnsureCapacity(vv, ww, xx, yy, zz);
    }
    public Integer[] makeInts(Integer i1) {
	Integer[] i = {new Integer(i1.intValue())};
	return i;
    }
    public Integer[] makeInts(Integer i1, Integer i2) {
    	Integer[] i = {new Integer(i1.intValue()), new Integer(i2.intValue())};
    	return i;
    }
    public Integer[] makeInts(Integer i1, Integer i2, Integer i3) {
    	Integer[] i = {new Integer(i1.intValue()), new Integer(i2.intValue()), new Integer(i3.intValue())};
    	return i;
    }
    public void setUp() {
        classUnderTest = new HashTable<>(INITIAL_SIZE);
    }

    public void testGetEmpty() {
        classUnderTest.clear();
        Assert.assertNull(classUnderTest.get(null));
    }

    public void testPutAndGet(Integer x, Integer y, Integer z) {
	Integer[3] is = makeInts(x, y, z);
        classUnderTest.clear();

        classUnderTest.put(x, y);
        classUnderTest.put(y, x);
        classUnderTest.put(z, x);
        Assert.assertEquals(classUnderTest.get(is[0]), is[1]);
        Assert.assertEquals(classUnderTest.get(is[1]), is[0]);
        Assert.assertEquals(classUnderTest.get(is[2]), is[0]);

    	Integer i = new Integer(x.intValue()+INITIAL_SIZE);
        classUnderTest.put(i, y);
        Assert.assertEquals(classUnderTest.get(i), y);
    }

    public void testReplacing(Integer x, Integer y, Integer z) {
	Integer[3] is = makeInts(x, y, z);
        classUnderTest.clear();
    	Integer i0 = new Integer(x.intValue()+INITIAL_SIZE);
    	Integer i1 = new Integer(x.intValue()+INITIAL_SIZE);
        classUnderTest.put(i0, z);
        Assert.assertEquals(classUnderTest.get(i1), is[2]);

        classUnderTest.put(x, y);
        Assert.assertEquals(classUnderTest.get(is[0]), is[1]);

        int size = classUnderTest.size();

        classUnderTest.put(x, z);
        Assert.assertEquals(classUnderTest.get(is[0]), is[2]);

    	classUnderTest.put(i0, z);
        Assert.assertEquals(classUnderTest.get(i1), is[2]);

        Assert.assertEquals(classUnderTest.size(), size);

    }

    public void testKeys(Integer x, Integer y) {
	Integer[2] is = makeInts(x, y);
        classUnderTest.clear();

        classUnderTest.put(x, y);
    	Object k = classUnderTest.keys()[0];
        Assert.assertEquals(k, is[0]);
    	// TODO: array access from method call as argument to assertTrue
        // Assert.assertEquals(classUnderTest.keys()[0], k);

    	// Object[] keys = classUnderTest.keys();
        // Assert.assertTrue(keys.length == 1);
     }

    // @Test
    public void testValues(Integer x, Integer y) {
	Integer[2] is = makeInts(x, y);
        classUnderTest.clear();

    	classUnderTest.put(x, y);
    	Object v = classUnderTest.values()[0];
    	Assert.assertEquals(v, is[1]);

        // Assert.assertTrue(k.equals(y));
    	// TODO: array access from method call as argument to assertTrue
        // Assert.assertEquals(classUnderTest.values()[0], k);
    }

    //TODO: why the heck is this so slow?! containsValue()????
    public void testContainsValue(Integer x, Integer y) {
	Integer[2] is = makeInts(x, y);
        classUnderTest.clear();

        classUnderTest.put(x, y);
    	Assert.assertTrue(classUnderTest.containsValue(is[1]));
    }

    public void testContainsKey(Integer x, Integer y) {
	Integer[2] is = makeInts(x, y);
        classUnderTest.clear();

        Assert.assertFalse(classUnderTest.containsKey(x));
        classUnderTest.put(x, y);
	// Integer i = new Integer(x.intValue());
    	Assert.assertTrue(classUnderTest.containsKey(is[0]));
    }

    public void testSize(int x, int y) {
    	assume x >= INITIAL_SIZE && x < 0;
        classUnderTest.clear();

    	// had to reduce loop size from original (2048)
    	for (int i = 0; i < INITIAL_SIZE; i++) { classUnderTest.put(new Integer(i), null); }
        Assert.assertEquals(classUnderTest.size(), INITIAL_SIZE);
        classUnderTest.put(new Integer(x), new Integer(y));
        Assert.assertEquals(classUnderTest.size(), INITIAL_SIZE+1);
    }

    public void testRemoveNonExistent(Integer x, Integer y) {
	Integer[2] is = makeInts(x, y);
        classUnderTest.clear();

        classUnderTest.put(x, y);
        int size = classUnderTest.size();
        classUnderTest.remove(is[1]);
        Assert.assertEquals(classUnderTest.size(), size);
    }

    public void testRemove(Integer x, Integer y) {
	Integer[2] is = makeInts(x, y);
        classUnderTest.clear();

        int size = classUnderTest.size();
        classUnderTest.put(x, y);

        Assert.assertEquals(classUnderTest.get(is[0]), is[1]);
        Assert.assertEquals(classUnderTest.size(), size + 1);

        classUnderTest.remove(x);
        Assert.assertNull(classUnderTest.get(is[0]));
    }

    public void testClear(Integer x, Integer y) {
    	classUnderTest.clear();

        classUnderTest.put(x, y);
        classUnderTest.put(y, x);
        Assert.assertTrue(classUnderTest.size() > 0);
        
    	classUnderTest.clear();
    	Asset.assertNull(classUnderTest.buckets.get(classUnderTest.initialCapacity-1));
    	Assert.assertFalse(classUnderTest.size() > 0);
    }

    public void testEnsureCapacity(Integer v, Integer w, Integer x, Integer y, Integer z) {
    	classUnderTest.clear();

        classUnderTest.put(v, w);
        classUnderTest.put(w, x);
        classUnderTest.put(x, y);
        classUnderTest.put(y, z);
        classUnderTest.put(z, v);
	
        Assert.assertEquals(classUnderTest.get(v), w);
        Assert.assertEquals(classUnderTest.get(w), x);
        Assert.assertEquals(classUnderTest.get(x), y);
        Assert.assertEquals(classUnderTest.get(y), z);
        Assert.assertEquals(classUnderTest.get(z), v);
    }
}

// ORIGINAL TESTS
// package com.anthonynsimon.datastructures;

// import org.junit.Before;
// import org.junit.Test;

// import java.util.Random;
// import java.util.UUID;

// import static org.junit.Assert.*;

// public class HashTableTest {

//     private HashTable<Object, Object> classUnderTest;

//     @Before
//     public void setUp() {
//         classUnderTest = new HashTable<>();

//         Random rand = new Random();
//         for (int i = 0; i < 2048; i++) {
//             classUnderTest.put(UUID.randomUUID().toString(), rand.nextInt(2048));
//         }
//     }

//     @Test
//     public void testGetEmpty() {
//         assertNull(classUnderTest.get(null));
//     }

//     @Test(expected = IllegalArgumentException.class)
//     public void testPutNull() throws IllegalArgumentException {
//         classUnderTest.put(null, 100);
//     }

//     @Test
//     public void testPutAndGet() {
//         classUnderTest.put("hey", "there");
//         classUnderTest.put(79514, "you");
//         classUnderTest.put("mac", 72);

//         assertEquals(classUnderTest.get("hey"), "there");
//         assertEquals(classUnderTest.get(79514), "you");
//         assertEquals(classUnderTest.get("mac"), 72);
//     }

//     @Test
//     public void testReplacing() {
//         classUnderTest.put("hey", "there");
//         assertEquals(classUnderTest.get("hey"), "there");

//         int size = classUnderTest.size();

//         classUnderTest.put("hey", "you");
//         assertEquals(classUnderTest.get("hey"), "you");

//         assertEquals(classUnderTest.size(), size);
//     }

//     @Test
//     public void testKeys() {
//         classUnderTest.clear();
//         assertArrayEquals(classUnderTest.keys(), new Object[]{});

//         classUnderTest.put("what", "there");

//         assertTrue(classUnderTest.keys()[0] == "what");

//         classUnderTest.put("that", "there");
//         classUnderTest.put("this", "there");
//         classUnderTest.put(452, "there");

//         assertTrue(classUnderTest.keys().length == 4);
//     }

//     @Test
//     public void testValues() {
//         classUnderTest.clear();
//         assertArrayEquals(classUnderTest.values(), new Object[]{});

//         classUnderTest.put("what", "some");

//         assertTrue(classUnderTest.values()[0] == "some");

//         classUnderTest.put("that", "things");
//         classUnderTest.put("this", "are");
//         classUnderTest.put(452, "there");

//         assertTrue(classUnderTest.values().length == 4);
//     }

//     @Test
//     public void testContainsValue() {
//         assertFalse(classUnderTest.containsValue("there"));
//         assertFalse(classUnderTest.containsValue(79514));
//         assertFalse(classUnderTest.containsValue("you"));

//         classUnderTest.put("what", "there");
//         classUnderTest.put(155550, "you");
//         classUnderTest.put("hey", 79514);

//         assertTrue(classUnderTest.containsValue("there"));
//         assertTrue(classUnderTest.containsValue(79514));
//         assertTrue(classUnderTest.containsValue("you"));
//     }

//     @Test
//     public void testContainsKey() {
//         assertFalse(classUnderTest.containsKey("what"));
//         assertFalse(classUnderTest.containsKey(79514));
//         assertFalse(classUnderTest.containsKey("hey"));

//         classUnderTest.put("what", "there");
//         classUnderTest.put(79514, "you");
//         classUnderTest.put("hey", 72);

//         assertTrue(classUnderTest.containsKey("what"));
//         assertTrue(classUnderTest.containsKey(79514));
//         assertTrue(classUnderTest.containsKey("hey"));
//     }

//     @Test
//     public void testSize() {
//         assertEquals(classUnderTest.size(), 2048);
//         classUnderTest.put("hey", "you");
//         assertEquals(classUnderTest.size(), 2049);
//     }

//     @Test
//     public void testRemoveNonExistent() {
//         int size = classUnderTest.size();
//         classUnderTest.remove("hey");
//         assertEquals(classUnderTest.size(), size);
//     }

//     @Test
//     public void testRemove() {
//         int size = classUnderTest.size();
//         classUnderTest.put("hey", "there");

//         assertEquals(classUnderTest.get("hey"), "there");
//         assertEquals(classUnderTest.size(), size + 1);

//         classUnderTest.remove("hey");
//         assertEquals(classUnderTest.get("hey"), null);
//         assertEquals(classUnderTest.size(), size);

//         classUnderTest.put("hey", "a");
//         classUnderTest.put("hola", "b");
//         classUnderTest.put("hello", "c");
//         classUnderTest.put("mac", "d");

//         assertEquals(classUnderTest.get("hola"), "b");
//         assertEquals(classUnderTest.size(), size + 4);

//         classUnderTest.remove("hola");

//         assertEquals(classUnderTest.get("hello"), "c");
//         assertEquals(classUnderTest.get("mac"), "d");
//         assertEquals(classUnderTest.get("hey"), "a");
//         assertEquals(classUnderTest.size(), size + 3);
//     }

//     @Test
//     public void testClear() {
//         assertTrue(classUnderTest.size() > 0);

//         classUnderTest.clear();

//         assertFalse(classUnderTest.size() > 0);
//         assertArrayEquals(classUnderTest.keys(), new Object[]{});
//         assertArrayEquals(classUnderTest.values(), new Object[]{});
//     }
// }

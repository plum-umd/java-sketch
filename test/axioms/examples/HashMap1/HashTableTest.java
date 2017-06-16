// This code is from https://github.com/anthonynsimon/java-ds-algorithms

// All tests take 10m to pass.

import org.junit.Before;
import org.junit.Test;

import java.util.Random;
import java.util.UUID;

import org.junit.Assert;


public class HashTableTest {
     // static so it will be initialised when translated
    public static final int INITIAL_SIZE = 16;

    private HashTable<Object, Object> classUnderTest;

    harness void mn(int x, int y, int z) {
	assume x != y && x != z && y != z;
	Integer xx = new Integer(x);
	Integer yy = new Integer(y);
	Integer zz = new Integer(z);
	setUp();
	testGetEmpty();
	testPutAndGet(xx, yy, zz);
	testReplacing(xx, yy, zz);
	testKeys(xx, yy);
	testValues(xx, yy);
	testContainsValue(xx, yy);
	testContainsKey(xx, yy);
	testRemoveNonExistent(xx, yy);
	testRemove(xx, yy);
	testClear(xx, yy);
	if (x >= INITIAL_SIZE && x < 0) { testSize(x, y); }
    }
    public void setUp() {
        classUnderTest = new HashTable<>(INITIAL_SIZE);
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
    }

    public void testReplacing(Integer x, Integer y, Integer z) {
        classUnderTest.clear();

        classUnderTest.put(x, y);
        Assert.assertEquals(classUnderTest.get(x), y);

        int size = classUnderTest.size();

        classUnderTest.put(x, z);
        Assert.assertEquals(classUnderTest.get(x), z);

        Assert.assertEquals(classUnderTest.size(), size);
    }

    public void testKeys(Integer x, Integer y) {
        classUnderTest.clear();

        classUnderTest.put(x, y);
	Object k = classUnderTest.keys()[0];
        Assert.assertTrue(k.equals(x));
	// TODO: array access from method call as argument to assertTrue
        // Assert.assertEquals(classUnderTest.keys()[0], k);

	Object[] keys = classUnderTest.keys();
        Assert.assertTrue(keys.length == 1);
     }

    // @Test
    public void testValues(Integer x, Integer y) {
        classUnderTest.clear();
        classUnderTest.put(x, y);

	Object k = classUnderTest.values()[0];
        Assert.assertTrue(k.equals(y));
	// TODO: array access from method call as argument to assertTrue
        // Assert.assertEquals(classUnderTest.values()[0], k);
    }

    //TODO: why the heck is this so slow?! containsValue()????
    public void testContainsValue(Integer x, Integer y) {
        classUnderTest.clear();

        Assert.assertFalse(classUnderTest.containsValue(y));
        classUnderTest.put(x, y);
	Assert.assertTrue(classUnderTest.containsValue(y));
    }

    public void testContainsKey(Integer x, Integer y) {
        classUnderTest.clear();

        Assert.assertFalse(classUnderTest.containsKey(x));
        classUnderTest.put(x, y);
	Assert.assertTrue(classUnderTest.containsKey(x));
    }

    public void testSize(int x, int y) {
	assume x >= INITIAL_SIZE && x < 0;
        classUnderTest.clear();

	// had to reduce loop size from original (2048)
	for (int i = 0; i < INITIAL_SIZE; i++) { classUnderTest.put(new Integer(i), null); }
        Assert.assertEquals(classUnderTest.size(), INITIAL_SIZE);
        classUnderTest.put(new Integer(x), new Integer(y));
        Assert.assertEquals(classUnderTest.size(), 17);
    }

    public void testRemoveNonExistent(Integer x, Integer y) {
        classUnderTest.clear();

        classUnderTest.put(x, y);
        int size = classUnderTest.size();
        classUnderTest.remove(y);
        Assert.assertEquals(classUnderTest.size(), size);
    }

    public void testRemove(Integer x, Integer y) {
        classUnderTest.clear();

        int size = classUnderTest.size();
        classUnderTest.put(x, y);

        Assert.assertEquals(classUnderTest.get(x), y);
        Assert.assertEquals(classUnderTest.size(), size + 1);

        classUnderTest.remove(x);
        Assert.assertNull(classUnderTest.get(x));
    }

    public void testClear(Integer x, Integer y) {
        classUnderTest.put(x, y);
        classUnderTest.put(y, x);
        Assert.assertTrue(classUnderTest.size() > 0);
        
	classUnderTest.clear();
	Asset.assertNull(classUnderTest.buckets.get(classUnderTest.initialCapacity-1));
	Assert.assertFalse(classUnderTest.size() > 0);
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

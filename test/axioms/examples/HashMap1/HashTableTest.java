// This code is from https://github.com/anthonynsimon/java-ds-algorithms

import org.junit.Before;
import org.junit.Test;

import java.util.Random;
import java.util.UUID;

import org.junit.Assert;

public class HashTableTest {

    private HashTable<Object, Object> classUnderTest16;
    private HashTable<Object, Object> classUnderTest32;

    harness void mn(int x, int y, int z) {
	Integer xx = new Integer(x);
	Integer yy = new Integer(y);
	Integer zz = new Integer(z);
	setUp();
	// testGetEmpty();
	testPutAndGet(xx, yy, zz);
	// testReplacing(xx, yy, zz);
	// testKeys(xx, yy);
	testValues(xx, yy);
	// testContainsValue(xx, yy, zz);
	// testContainsKey(xx, yy, zz);
	// testRemoveNonExistent(xx);
	testRemove(xx, yy, zz);
	testClear(xx, yy);
	// assume x >= 16 && x < 0;
	// testSize(x, y);
    }
    public void setUp() {
        classUnderTest16 = new HashTable<>(16);
    }

    public void testGetEmpty() {
	Object o = classUnderTest16.get(null);
        Assert.assertNull(classUnderTest16.get(null));
    }

    public void testPutAndGet(Integer x, Integer y, Integer z) {
        classUnderTest16.put(x, y);
        classUnderTest16.put(y, x);
        // classUnderTest16.put(z, x);
        Assert.assertEquals(classUnderTest16.get(x), y);
        Assert.assertEquals(classUnderTest16.get(y), x);
        // Assert.assertEquals(classUnderTest16.get(z), x);
    }

    public void testReplacing(Integer x, Integer y, Integer z) {
        classUnderTest16.put(x, x);
        Assert.assertEquals(classUnderTest16.get(x), x);

        int size = classUnderTest16.size();

        classUnderTest16.put(x, z);
        Assert.assertEquals(classUnderTest16.get(x), z);

        Assert.assertEquals(classUnderTest16.size(), size);
    }

    public void testKeys(Integer x, Integer y) {
        classUnderTest16.clear();

        classUnderTest16.put(x, y);
	Object k = classUnderTest16.keys()[0];
        Assert.assertTrue(k.equals(x));
	// TODO: array access from method call as argument to assertTrue
        // Assert.assertEquals(classUnderTest16.keys()[0], k);

	Object[] keys = classUnderTest16.keys();
        Assert.assertTrue(keys.length == 1);
     }

    // @Test
    public void testValues(Integer x, Integer y) {
        classUnderTest16.clear();
        classUnderTest16.put(x, y);

	Object k = classUnderTest16.values()[0];
        Assert.assertTrue(k.equals(y));
	// TODO: array access from method call as argument to assertTrue
        // Assert.assertEquals(classUnderTest16.values()[0], k);
    }

    //TODO: why the heck is this so slow?! containsValue()????
    public void testContainsValue(Integer x, Integer y, Integer z) {
        classUnderTest16.clear();
        classUnderTest16.put(x, y);
	Assert.assertTrue(classUnderTest16.containsValue(y));
    }

    public void testContainsKey(Integer x, Integer y, Integer z) {
        classUnderTest16.clear();
        Assert.assertFalse(classUnderTest16.containsKey(x));
        classUnderTest16.put(x, y);
	Assert.assertTrue(classUnderTest16.containsKey(x));
    }

    public void testSize(int x, int y) {
	// had to reduce loop size from original (2048)
	for (int i = 0; i < 16; i++) { classUnderTest16.put(new Integer(i), null); }
        Assert.assertEquals(classUnderTest16.size(), 16);
        classUnderTest16.put(new Integer(x), new Integer(y));
        Assert.assertEquals(classUnderTest16.size(), 17);
    }

    public void testRemoveNonExistent(Integer x) {
        int size = classUnderTest16.size();
        classUnderTest16.remove(x);
        Assert.assertEquals(classUnderTest16.size(), size);
    }

    public void testRemove(Integer x, Integer y, Integer z) {
        classUnderTest16.clear();

        int size = classUnderTest16.size();
        classUnderTest16.put(x, y);

        Assert.assertEquals(classUnderTest16.get(x), y);
        Assert.assertEquals(classUnderTest16.size(), size + 1);

        classUnderTest16.remove(x);
        Assert.assertNull(classUnderTest16.get(x));
    }

    public void testClear(Integer x, Integer y) {
        classUnderTest16.put(x, y);
        classUnderTest16.put(y, x);
        Assert.assertTrue(classUnderTest16.size() > 0);
        
	classUnderTest16.clear();
	Asset.assertNull(classUnderTest16.buckets.get(classUnderTest16.initialCapacity-1));
	Assert.assertFalse(classUnderTest16.size() > 0);
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

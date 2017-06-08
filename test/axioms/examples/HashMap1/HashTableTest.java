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
	// Integer zz = new Integer(z);
	setUp();
	// testGetEmpty();
	// testPutAndGet(xx, yy, zz);
	// testReplacing(xx, yy, zz);
	// testKeys(xx, yy);
	testSize();
	// testClear(xx, yy, zz);
    }
    // Not sure about random in Sketch
    // @Before
    public void setUp() {
        classUnderTest16 = new HashTable<>(16);
        // classUnderTest32 = new HashTable<>(32);

    //     Random rand = new Random();
    //     for (int i = 0; i < 2048; i++) {
    //         classUnderTest16.put(UUID.randomUUID().toString(), rand.nextInt(2048));
    //     }
    }

    @Test
    public void testGetEmpty() {
	Object o = classUnderTest16.get(null);
        Assert.assertNull(classUnderTest16.get(null));
    }

    @Test
    public void testPutAndGet(Integer x, Integer y, Integer z) {
        classUnderTest16.put(x, y);
        classUnderTest16.put(y, x);
        Assert.assertEquals(classUnderTest16.get(x), y);
        Assert.assertEquals(classUnderTest16.get(y), x);

	// classUnderTest32.put(x, y);
        // classUnderTest32.put(y, x);
        // classUnderTest32.put(z, x);
        // Assert.assertEquals(classUnderTest32.get(x), y);
        // Assert.assertEquals(classUnderTest32.get(y), x);
        // Assert.assertEquals(classUnderTest32.get(z), x);
    }

    // @Test
    public void testReplacing(Integer x, Integer y, Integer z) {
        classUnderTest16.put(x, x);
        Assert.assertEquals(classUnderTest16.get(x), x);

        int size = classUnderTest16.size();

        classUnderTest16.put(x, z);
        Assert.assertEquals(classUnderTest16.get(x), z);

        Assert.assertEquals(classUnderTest16.size(), size);
    }

    // @Test
    public void testKeys(Integer x, Integer y) {
        classUnderTest16.clear();
        // Assert.assertArrayEquals(classUnderTest16.keys(), new Object[]{}); // assertArrayEquals not implemented in JSKetch

        classUnderTest16.put(x, y);
	Object k = classUnderTest16.keys()[0];
        Assert.assertTrue(k.equals(x));
	// TODO: fix this vvvv
        // Assert.assertEquals(classUnderTest16.keys()[0], k);

        // classUnderTest16.put("that", "there");
        // classUnderTest16.put("this", "there");
        // classUnderTest16.put(new Integer(452), "there");

	Object[] keys = classUnderTest16.keys();
        Assert.assertTrue(keys.length == 1);
     }

    // @Test
    // public void testValues() {
    //     classUnderTest16.clear();
    //     Assert.assertArrayEquals(classUnderTest16.values(), new Object[]{});

    //     classUnderTest16.put("what", "some");

    //     Assert.assertTrue(classUnderTest16.values()[0] == "some");

    //     classUnderTest16.put("that", "things");
    //     classUnderTest16.put("this", "are");
    //     classUnderTest16.put(452, "there");

    //     Assert.assertTrue(classUnderTest16.values().length == 4);
    // }

    // @Test
    // public void testContainsValue() {
    //     Assert.assertFalse(classUnderTest16.containsValue("there"));
    //     Assert.assertFalse(classUnderTest16.containsValue(79514));
    //     Assert.assertFalse(classUnderTest16.containsValue("you"));

    //     classUnderTest16.put("what", "there");
    //     classUnderTest16.put(155550, "you");
    //     classUnderTest16.put("hey", 79514);

    //     Assert.assertTrue(classUnderTest16.containsValue("there"));
    //     Assert.assertTrue(classUnderTest16.containsValue(79514));
    //     Assert.assertTrue(classUnderTest16.containsValue("you"));
    // }

    // @Test
    // public void testContainsKey() {
    //     Assert.assertFalse(classUnderTest16.containsKey("what"));
    //     Assert.assertFalse(classUnderTest16.containsKey(79514));
    //     Assert.assertFalse(classUnderTest16.containsKey("hey"));

    //     classUnderTest16.put("what", "there");
    //     classUnderTest16.put(79514, "you");
    //     classUnderTest16.put("hey", 72);

    //     Assert.assertTrue(classUnderTest16.containsKey("what"));
    //     Assert.assertTrue(classUnderTest16.containsKey(79514));
    //     Assert.assertTrue(classUnderTest16.containsKey("hey"));
    // }

    // @Test
    public void testSize() {
	// had to reduce loop size from original (2048)
	for (int i = 0; i < 16; i++) { classUnderTest16.put(new Integer(i), null); }
        Assert.assertEquals(classUnderTest16.size(), 16);
        classUnderTest16.put("hey", "you");
        Assert.assertEquals(classUnderTest16.size(), 17);
    }

    // @Test
    // public void testRemoveNonExistent() {
    //     int size = classUnderTest16.size();
    //     classUnderTest16.remove("hey");
    //     Assert.assertEquals(classUnderTest16.size(), size);
    // }

    // @Test
    // public void testRemove() {
    //     int size = classUnderTest16.size();
    //     classUnderTest16.put("hey", "there");

    //     Assert.assertEquals(classUnderTest16.get("hey"), "there");
    //     Assert.assertEquals(classUnderTest16.size(), size + 1);

    //     classUnderTest16.remove("hey");
    //     Assert.assertEquals(classUnderTest16.get("hey"), null);
    //     Assert.assertEquals(classUnderTest16.size(), size);

    //     classUnderTest16.put("hey", "a");
    //     classUnderTest16.put("hola", "b");
    //     classUnderTest16.put("hello", "c");
    //     classUnderTest16.put("mac", "d");

    //     Assert.assertEquals(classUnderTest16.get("hola"), "b");
    //     Assert.assertEquals(classUnderTest16.size(), size + 4);

    //     classUnderTest16.remove("hola");

    //     Assert.assertEquals(classUnderTest16.get("hello"), "c");
    //     Assert.assertEquals(classUnderTest16.get("mac"), "d");
    //     Assert.assertEquals(classUnderTest16.get("hey"), "a");
    //     Assert.assertEquals(classUnderTest16.size(), size + 3);
    // }

    // @Test
    public void testClear(Integer x, Integer y, Integer z) {
        Assert.assertTrue(classUnderTest16.size() > 0);
        
	classUnderTest16.clear();
	assert classUnderTest16.buckets.get(classUnderTest16.initialCapacity-1) == null;
	Assert.assertFalse(classUnderTest16.size() > 0);

        // Assert.assertTrue(classUnderTest32.size() > 0);
	// classUnderTest32.clear();
	// assert classUnderTest32.buckets.get(classUnderTest32.initialCapacity-1) == null;
        // Assert.assertArrayEquals(classUnderTest16.keys(), new Object[]{});
        // Assert.assertArrayEquals(classUnderTest16.values(), new Object[]{});
    }
}


    // @Test(expected = IllegalArgumentException.class)
    // public void testPutNull() throws IllegalArgumentException {
    //     classUnderTest16.put(null, 100);
    // }

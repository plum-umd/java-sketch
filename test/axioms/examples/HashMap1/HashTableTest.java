// This code is from https://github.com/anthonynsimon/java-ds-algorithms

import org.junit.Before;
import org.junit.Test;

import java.util.Random;
import java.util.UUID;

import org.junit.Assert;

public class HashTableTest {

    private HashTable<Object, Object> classUnderTest;
    harness void mn() {
	setUp();
	testPutAndGet();
    }
    // Not sure about random in Sketch
    // @Before
    public void setUp() {
        classUnderTest = new HashTable<>();

    //     Random rand = new Random();
    //     for (int i = 0; i < 2048; i++) {
    //         classUnderTest.put(UUID.randomUUID().toString(), rand.nextInt(2048));
    //     }
    }

    @Test
    public void testGetEmpty() {
	Object o = classUnderTest.get(null);
        // Assert.assertNull(null);
        // Assert.assertNull(classUnderTest.get(null));
    }

    // @Test(expected = IllegalArgumentException.class)
    // public void testPutNull() throws IllegalArgumentException {
    //     classUnderTest.put(null, 100);
    // }

    @Test
    public void testPutAndGet() {
        classUnderTest.put("hey", "there");
        // classUnderTest.put(79514, "you");
        // classUnderTest.put("mac", 72);

        // Assert.assertEquals(classUnderTest.get("hey"), "there");
        // Assert.assertEquals(classUnderTest.get(79514), "you");
        // Assert.assertEquals(classUnderTest.get("mac"), 72);
    }

    // @Test
    // public void testReplacing() {
    //     classUnderTest.put("hey", "there");
    //     Assert.assertEquals(classUnderTest.get("hey"), "there");

    //     int size = classUnderTest.size();

    //     classUnderTest.put("hey", "you");
    //     Assert.assertEquals(classUnderTest.get("hey"), "you");

    //     Assert.assertEquals(classUnderTest.size(), size);
    // }

    // @Test
    // public void testKeys() {
    //     classUnderTest.clear();
    //     Assert.assertArrayEquals(classUnderTest.keys(), new Object[]{});

    //     classUnderTest.put("what", "there");

    //     Assert.assertTrue(classUnderTest.keys()[0] == "what");

    //     classUnderTest.put("that", "there");
    //     classUnderTest.put("this", "there");
    //     classUnderTest.put(452, "there");

    //     Assert.assertTrue(classUnderTest.keys().length == 4);
    // }

    // @Test
    // public void testValues() {
    //     classUnderTest.clear();
    //     Assert.assertArrayEquals(classUnderTest.values(), new Object[]{});

    //     classUnderTest.put("what", "some");

    //     Assert.assertTrue(classUnderTest.values()[0] == "some");

    //     classUnderTest.put("that", "things");
    //     classUnderTest.put("this", "are");
    //     classUnderTest.put(452, "there");

    //     Assert.assertTrue(classUnderTest.values().length == 4);
    // }

    // @Test
    // public void testContainsValue() {
    //     Assert.assertFalse(classUnderTest.containsValue("there"));
    //     Assert.assertFalse(classUnderTest.containsValue(79514));
    //     Assert.assertFalse(classUnderTest.containsValue("you"));

    //     classUnderTest.put("what", "there");
    //     classUnderTest.put(155550, "you");
    //     classUnderTest.put("hey", 79514);

    //     Assert.assertTrue(classUnderTest.containsValue("there"));
    //     Assert.assertTrue(classUnderTest.containsValue(79514));
    //     Assert.assertTrue(classUnderTest.containsValue("you"));
    // }

    // @Test
    // public void testContainsKey() {
    //     Assert.assertFalse(classUnderTest.containsKey("what"));
    //     Assert.assertFalse(classUnderTest.containsKey(79514));
    //     Assert.assertFalse(classUnderTest.containsKey("hey"));

    //     classUnderTest.put("what", "there");
    //     classUnderTest.put(79514, "you");
    //     classUnderTest.put("hey", 72);

    //     Assert.assertTrue(classUnderTest.containsKey("what"));
    //     Assert.assertTrue(classUnderTest.containsKey(79514));
    //     Assert.assertTrue(classUnderTest.containsKey("hey"));
    // }

    // @Test
    // public void testSize() {
    //     Assert.assertEquals(classUnderTest.size(), 2048);
    //     classUnderTest.put("hey", "you");
    //     Assert.assertEquals(classUnderTest.size(), 2049);
    // }

    // @Test
    // public void testRemoveNonExistent() {
    //     int size = classUnderTest.size();
    //     classUnderTest.remove("hey");
    //     Assert.assertEquals(classUnderTest.size(), size);
    // }

    // @Test
    // public void testRemove() {
    //     int size = classUnderTest.size();
    //     classUnderTest.put("hey", "there");

    //     Assert.assertEquals(classUnderTest.get("hey"), "there");
    //     Assert.assertEquals(classUnderTest.size(), size + 1);

    //     classUnderTest.remove("hey");
    //     Assert.assertEquals(classUnderTest.get("hey"), null);
    //     Assert.assertEquals(classUnderTest.size(), size);

    //     classUnderTest.put("hey", "a");
    //     classUnderTest.put("hola", "b");
    //     classUnderTest.put("hello", "c");
    //     classUnderTest.put("mac", "d");

    //     Assert.assertEquals(classUnderTest.get("hola"), "b");
    //     Assert.assertEquals(classUnderTest.size(), size + 4);

    //     classUnderTest.remove("hola");

    //     Assert.assertEquals(classUnderTest.get("hello"), "c");
    //     Assert.assertEquals(classUnderTest.get("mac"), "d");
    //     Assert.assertEquals(classUnderTest.get("hey"), "a");
    //     Assert.assertEquals(classUnderTest.size(), size + 3);
    // }

    // @Test
    // public void testClear() {
    //     Assert.assertTrue(classUnderTest.size() > 0);

    //     classUnderTest.clear();

    //     Assert.assertFalse(classUnderTest.size() > 0);
    //     Assert.assertArrayEquals(classUnderTest.keys(), new Object[]{});
    //     Assert.assertArrayEquals(classUnderTest.values(), new Object[]{});
    // }
}

// This code is from https://github.com/anthonynsimon/java-ds-algorithms

import org.junit.Before;
import org.junit.Test;

import java.util.EmptyStackException;

import org.junit.Assert;

public class StackTest {

    private Stack<Integer> classUnderTest;

    @Before
    public harness void setUp(int x, int y, int z) {
        classUnderTest = new Stack<>();
	testEmptyStack();
	Integer xx = new Integer(x);
	Integer yy = new Integer(y);
	Integer zz = new Integer(z);
	testPushingElements(xx, yy);
	testPoppingElements(xx, yy);
	testPeeking(xx, yy);
	testClear(xx, yy, zz);
    }
    
    @Test(expected = EmptyStackException.class)
    public void testEmptyStack() {
        Assert.assertEquals(classUnderTest.size(), 0);

        // Pop empty stack, will throw exception
        // classUnderTest.pop();
    }

    @Test
    public void testPushingElements(Integer x, Integer y) {
        classUnderTest.push(x);
        Assert.assertEquals(classUnderTest.size(), 1);

        classUnderTest.push(y);
        Assert.assertEquals(classUnderTest.size(), 2);
    }

    @Test(expected = EmptyStackException.class)
    public void testPoppingElements(Integer x, Integer y) {
        classUnderTest.push(x);
        classUnderTest.push(y);

        Assert.assertEquals(classUnderTest.pop(), y);
        Assert.assertEquals(classUnderTest.pop(), x);
        // classUnderTest.pop();
    }

    // @Test
    // public void testToString() {
    //     classUnderTest.push("you");
    //     classUnderTest.push("there");
    //     classUnderTest.push("hello");

    //     assertEquals(classUnderTest.toString(", "), "hello, there, you");

    //     classUnderTest.push("hola!, ");

    //     assertEquals(classUnderTest.toString(), "hola!, hellothereyou");
    // }

    @Test(expected = EmptyStackException.class)
    public void testPeeking(Integer x, Integer y) {
        classUnderTest.clear();
        classUnderTest.push(x);
        classUnderTest.push(y);

        Assert.assertEquals(classUnderTest.peek(), y);
        classUnderTest.pop();
        Assert.assertEquals(classUnderTest.peek(), x);

        // Pop last element
        // classUnderTest.pop();
        // Peek empty stack, will throw exception
        // classUnderTest.peek();
    }

    @Test
    public void testClear(Integer x, Integer y, Integer z) {
        classUnderTest.clear();

        Assert.assertEquals(classUnderTest.size(), 0);

        classUnderTest.push(x);
        classUnderTest.push(y);
        classUnderTest.push(z);

        Assert.assertEquals(classUnderTest.size(), 3);

        classUnderTest.clear();

        Assert.assertEquals(classUnderTest.size(), 0);
    }
}

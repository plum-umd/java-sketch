import org.junit.Assert;

class StaticImport {
    harness void mn() {
	String s = "h";
	String s1 = "h";
	Object o = new Object();
	Assert.assertEquals(o, o);
    }
}

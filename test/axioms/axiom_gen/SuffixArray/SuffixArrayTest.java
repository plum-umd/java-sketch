public class SuffixArrayTest {

    harness public void main() {
	testLRS();
    }
    
  @Before
  public void setup() { }
    
  @Test
  public void testLRS() {

    String s = "aabaab";
    boolean cont1 = false;
    boolean cont2 = false;
    SuffixArray sa = new SuffixArray(s);
    TreeSet <String> lrss = sa.lrs();
    assert 1 == lrss.size();
    cont1 = lrss.contains("aab");
    assert cont1;

    s = "abcba";
    sa = new SuffixArray(s);
    lrss = sa.lrs();
    assert lrss.size() == 2;
    assert lrss.contains("a");
    assert lrss.contains("b");

    s = "abccdd";
    sa = new SuffixArray(s);
    lrss = sa.lrs();
    assert lrss.size() == 2;
    assert lrss.contains("c");
    assert lrss.contains("d");    

    s = "aaab";
    sa = new SuffixArray(s);
    lrss = sa.lrs();
    assert lrss.size() == 1;
    assert lrss.contains("aa");

    s = "ababa";	
    sa = new SuffixArray(s);
    lrss = sa.lrs();
    assert lrss.size() == 1;
    assert lrss.contains("aba");    
    
  }
}

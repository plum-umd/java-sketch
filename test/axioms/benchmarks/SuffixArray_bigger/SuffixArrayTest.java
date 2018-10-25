// import static org.junit.Assert.*;
// import org.junit.*;

// import java.security.SecureRandom;
// import java.math.BigInteger;
// import java.util.Random;
// import java.util.Arrays;
// import java.util.List;
// import java.util.ArrayList;
// import java.util.Set;

public class SuffixArrayTest {

  // static final SecureRandom random = new SecureRandom();
  // static final Random rand = new Random();

  // static final int LOOPS = 1000;
  // static final int TEST_SZ = 5057;
  // static final int NUM_NULLS = TEST_SZ / 5;
  // static final int MAX_RAND_NUM = 250;

    // harness public void main(int x, int y ) {
    harness public void main() {
	// containsSubstring();
	testLRS();
      // testLCS();
  }
    
  @Before
  public void setup() { }

  // @Test
  // public void testContruction() {

    // for (int i = 0; i < LOOPS; i++) {
      
    //   String r = randomString(randNum(1, TEST_SZ));

    //   SuffixArray sa = new SuffixArray(r);
    //   SuffixArrayNaive san = new SuffixArrayNaive(r);
    //   SuffixArrayFast saf = new SuffixArrayFast(r);

    //   int[] sa_arr = sa.sa; //getSuffixPositions();
    //   int[] san_arr = san.getSuffixPositions();
    //   int[] saf_arr = saf.sa;

    //   for (int k = 0; k < sa.N; k++ ) {
    //     assertEquals(san_arr[k], sa_arr[k]);
    //     assertEquals(saf_arr[k], sa_arr[k]);
    //   }

    // }

  // }

  // @Test 
  // public void containsSubstring() {

  //   String s = "abcdef";
  //   SuffixArray sa = new SuffixArray(s);
  //   // SuffixArrayFast saf = new SuffixArrayFast(s);
    
  //   Assert.assertTrue( sa.contains("") );

  //   for (int i = 0; i < s.length(); i++ ) {
  //     for (int j = i+1; j <= s.length(); j++ ) {
  //       String substr = s.substring(i, j);
  //       Assert.assertTrue(sa.contains(substr));
  //       // Assert.assertTrue(saf.contains(substr));
  //     }
  //   }

  //   Assert.assertFalse( sa.contains("abce") );
  //   Assert.assertFalse( sa.contains("efg") );
  //   Assert.assertFalse( sa.contains("aaa") );
  //   Assert.assertFalse( sa.contains("y") );

  // }

  // @Test
  // public void testLRS_gen(int x, int y) {
  //   assume x >= 1 && x < 10;
  //   assume y >= 1 && y < 10;
      
  //   String s = Integer.toString(x);
  //   String total = Integer.toString((x*10)+x);
  //   String cont = Integer.toString(x);
  //   for (int i = 0; i < y; i++) {
  // 	SuffixArray sa = new SuffixArray(total);
  // 	TreeSet <String> lrss = sa.lrs();
  // 	// list.addAll(lrss);
  // 	//CHANGE
  // 	assert 1 == lrss.size();
  // 	// assertEquals(1, lrss.size());
  // 	// // CHANGE
  // 	assert lrss.contains(cont);
  // 	cont.concat(s);
  // 	// // assertEquals("aab", list.get(0));
  // 	// // list.clear();
  // 	total.concat(s);
  //   }
  // }
    
  @Test
  public void testLRS() {

    String s = "aabaab";
    boolean cont1 = false;
    boolean cont2 = false;
    SuffixArray sa = new SuffixArray(s);
    TreeSet <String> lrss = sa.lrs();
    // list.addAll(lrss);
    //CHANGE
    assert 1 == lrss.size();
    // assertEquals(1, lrss.size());
    // // CHANGE
    cont1 = lrss.contains("aab");
    assert cont1;
    // // assertEquals("aab", list.get(0));
    // // list.clear();

    // s = "abcdefg";
    // sa = new SuffixArray(s);
    // lrss = sa.lrs();    
    // // list.addAll(lrss);
    // // CHANGE
    // assert lrss.size() == 0;
    // // assertEquals(0, list.size());
    // // list.clear();

    // s = "abca";
    // sa = new SuffixArray(s);
    // lrss = sa.lrs();
    // // list.addAll(lrss);
    // // CHANGE
    // assert lrss.size() == 1;
    // // assertEquals(1, lrss.size());
    // // CHANGE
    // cont1 = lrss.contains("a");
    // assert cont1;
    // // assertEquals("a", list.get(0));
    // // list.clear();

    s = "babababa";
    sa = new SuffixArray(s);
    lrss = sa.lrs();
    // list.addAll(lrss);
    // CHANGE
    assert lrss.size() == 1;
    // assertEquals(2, lrss.size() );
    // CHANGE
    assert lrss.contains("bababa");
    // assertEquals("b", list.get(1));
    // list.clear();
    
    s = "abcba";
    sa = new SuffixArray(s);
    lrss = sa.lrs();
    // list.addAll(lrss);
    // CHANGE
    assert lrss.size() == 2;
    // assertEquals(2, lrss.size() );
    // CHANGE
    assert lrss.contains("a");
    assert lrss.contains("b");
    // assertEquals("a", list.get(0));
    // assertEquals("b", list.get(1));
    // list.clear();

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
    // assert lrss.contains("ab");
    // assert lrss.contains("ba");    
    assert lrss.contains("aba");    
    
    // s = "aZZbZZcYYdYYe";
    // // s = "aZZbYY";
    // sa = new SuffixArray(s);
    // lrss = sa.lrs();
    // // list.addAll(lrss);
    // assert lrss.size() == 2;
    // // assertEquals(2, lrss.size() );
    // // CHANGE
    // assert lrss.contains("YY");
    // assert lrss.contains("ZZ");
    // // assertEquals("YY", list.get(0));
    // // assertEquals("ZZ", list.get(1));
    // // list.clear();

    // s = "AAAAAA";
    // sa = new SuffixArray(s);
    // lrss = sa.lrs();
    // // list.addAll(lrss);
    // // CHANGE
    // assert lrss.size() == 1;
    // // assertEquals(1, lrss.size() );
    // // CHANGE
    // assert lrss.contains("AAAAA");
    // // assertEquals("AAAAA", list.get(0));
    // // list.clear();

    // s = "aWXYZsdfABCDbvABCDsWXYZyWXYZjisdssd";
    // sa = new SuffixArray(s);
    // lrss = sa.lrs();
    // // list.addAll(lrss);
    // // CHANGE
    // assert lrss.size() == 2;
    // // assertEquals(2, lrss.size() );
    // // CHANGE
    // assert lrss.contains("ABCD");
    // assert lrss.contains("WXYZ");
    // // assertEquals("ABCD", list.get(0));
    // // assertEquals("WXYZ", list.get(1));
    // // list.clear();

  }

  // @Test
  // public void testRandomizedContains() {

  //   for (int loop = 1; loop < LOOPS; loop++) {
  //     String r = randomString(50);

  //     for (int i = 0; i < TEST_SZ ;i++ ) {
        
  //       int s = randNum(0, r.length()-1);
  //       int e = randNum(s, r.length()-1);
  //       if (s == e) continue;
  //       String substr = r.substring(s,e);
  //       SuffixArray sa = new SuffixArray( r );
  //       SuffixArrayFast saf = new SuffixArrayFast( r );
  //       Assert.assertTrue(sa.contains(substr));
  //       Assert.assertTrue(saf.contains(substr));

  //       String r2 = randomString(3);
  //       assertEquals( sa.contains(r2),  r.contains(r2));
  //       assertEquals( saf.contains(r2),  r.contains(r2));

  //     }

  //   }

  // }

  // @Test
  // public void testLCS() {
  //   String[] strs = {"abcde", "gear", "#"};
  //   String a = "a";
  //   TreeSet <String> lcss = SuffixArray.lcs(strs, 2);
    
  //   assert lcss.size() == 2;
  //     // assertEquals( SuffixArray.lcs(strs, 2), "a" );
  //   // assertEquals( SuffixArray.lcs("abcde", "xzy", '#'), null );
  //   // assertEquals( SuffixArray.lcs("cabbage", "garbage", '#'), "bage" );
  //   // assertEquals( SuffixArray.lcs("123-345-4566", "4-345-4566-7653", '#'), "-345-4566" );

  // }

  // static int randNum(int min, int max) {
  //   int range = max - min + 1;
  //   return rand.nextInt(range) + min;
  // }

  // static final String AB = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
  
  // static String randomString( int len ){
  //   StringBuilder sb = new StringBuilder( len );
  //   for( int i = 0; i < len; i++ ) 
  //      sb.append( AB.charAt( rand.nextInt(AB.length()) ) );
  //   return sb.toString();
  // }

}

// Example 1 from page 3 of Java Precisely third edition (The MIT Press 2016)
// Author: Peter Sestoft (sestoft@itu.dk)


class Example1 {
  // This is a one-line comment; it extends to the end of the line.
  /* This is a delimited comment,
     extending over several lines.
  */
  int /* This delimited comment extends over part of a line */ x = 117;
  
  harness static void test() {
      Example1 t = new Example1();
      t.x = 117;
      assert t.x == 117;
  }
}


class Node {
    public int x;
    public Node next;

    public Node(int x) {
        this.x = x;
    }
}

class Test {
    /**
     *      d
     *    /   \
     *   ?     ?
     *  c - b - a
     */
    harness static void test () {
        Node a = new Node(1);
        Node b = new Node(2);
        b.next = a;
        Node c = new Node(3);
        c.next = b;

        Node d = new Node(4);
        d.next = {| c | b |};

        Node iter = d.next;
        iter = iter.next;
        iter = iter.next; // due to this iteration, d should point to c, not b
        assert iter.x == 1;
    }
}

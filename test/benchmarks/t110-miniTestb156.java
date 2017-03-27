class MyQueue {
    Node head;
    Node tail;

    public MyQueue() {
        this.head = null;
        this.tail = null;
    }

    public generator Node select() {
        int t = ??;
        if (t == 0) {
            return this.tail;
        }
        if (t == 1) {
            return this.head;
        }
        if (t == 2) {
            Node n = select();
            assert n != null;
            return n.next;
        }
        return null;
    }
}

class Node {
    int x;
    Node next;

    public Node(int x) {
        this.x = x;
    }
}

class Test {
    harness static void test() {
        MyQueue q = new MyQueue();
        Node n0 = new Node(0);
        Node n1 = new Node(1);
        Node n2 = new Node(2);

        q.head = n0;
        q.head.next = n1;
        q.head.next.next = n2;
        q.tail = n2;

        assert q.head.next == q.select();
    }
}

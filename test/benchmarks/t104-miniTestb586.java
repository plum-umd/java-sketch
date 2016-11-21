class Tree {
    public final static int LEAF = 1;
    public final static int BRANCH = 2;

    public int kind;
    int value;

    public Tree (int value) {
        this.value = value;
    }
}

class Leaf extends Tree {
    public Leaf (int value) {
        this.kind = Tree.LEAF;
        super(value);
    }
}

// class Branch extends Tree {
//     public Tree left;
//     public Tree right;

//     public Branch (int value) {
//         this.kind = Tree.BRANCH;
//         super(value);
//     }
// }

class Testb586 {
    // public static int sum (Tree t) {
    //     switch (t.kind) {
    //         case Tree.LEAF:
    //             return t.value;
    //         case Tree.BRANCH:
    //             return t.value + sum(((Branch)t).left) + sum(((Branch)t).right);
    //     }
    // }

    harness static void test () {
        Leaf l1 = new Leaf(5);
	assert l1.value == 1;
        Leaf l2 = new Leaf(4);
        // Branch b = new Branch(2);
        // b.left = l1;
        // b.right = l2;

        // assert sum(b) == (5 + 4 + 2);
    }
}

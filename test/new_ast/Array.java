class MultiType {
    public MTArray lst;
    public int val;

    public MultiType(int val) {
      this.val = val;
    }
}

class MTArray {
    public MultiType[] A;
}

class Array {
    harness static void main() {
        MultiType mtype1 = new MultiType(5);
        MultiType mtype2 = new MultiType(10);

        MTArray mtarray = new MTArray();
        mtarray.A = new MultiType[] {mtype1, mtype2};

        MultiType mtype3 = new MultiType(0);
        mtype3.lst = mtarray;

        assert mtype3.lst.A[0].val == 5;
        assert mtype3.lst.A[1].val == 10;
    }
}

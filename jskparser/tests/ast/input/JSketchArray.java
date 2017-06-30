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

        MTArray mtarray = new MTArray();
        mtarray.A = new MultiType[] {mtype1};

        assert mtarray.lst.A[0].val == 5;
    }
}

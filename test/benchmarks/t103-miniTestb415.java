class MultiType {
    public MTArray lst;
    public int val;
    public int flag;

    public MultiType(int val, int flag) {
      this.val = val;
      this.flag = flag;
    }
}

class MTArray {
    public int len;
    public MultiType[] A;
}

class Testb415 {

    static int INTEGER = 0;
    static int LIST = 1;

    harness static void main() {
        MultiType x = new MultiType(5, Testb415.INTEGER);
        MultiType __y = new MultiType(10, Testb415.INTEGER);
        MTArray _y = new MTArray();
        _y.A = new MultiType[] {x, __y};
        _y.len = 2;
        MultiType y = new MultiType(0, Testb415.LIST);
        y.lst = _y;

        assert y.lst.A[0].val != y.lst.A[1].val;
    }
}

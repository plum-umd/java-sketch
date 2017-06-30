class C {
    int a(int a, int b, int c) {
        a = b + c;
        return a;
    }
    void b() {
        int x = 0, y = 1, z = 2;
        a(x, y, z);
    }
}


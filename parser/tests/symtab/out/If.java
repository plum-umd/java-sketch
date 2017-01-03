class If {
    void m() {
        int a = 0;
        if (a > 1) {
            a = 1;
        }
        if (a > 2) {
            a = 2;
        }
        else if (a > 3) {
            a = 3;
        }
        if (a > 4) {
            a = 4;
        }
        else if (a > 5) {
            if (a > 6) {
                a = 6;
            }
        }
        else {
            a = 7;
        }
        if (a > 8) {
            a = 8;
        }
        else {
            if (a > 9) {
                a = 9;
            }
        }
    }
}


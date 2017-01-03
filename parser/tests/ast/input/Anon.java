interface OnEvent {
    public void onEvent();
}

class ABC {
    public static int x;

    public static void tick() {
        x = x + 1;
    }

    public OnEvent handler;

    public ABC (int init_x) {
        ABC.x = init_x;

        handler = new OnEvent() {
            public void onEvent() {
                tick();
            }
        };
    }
}

class Test {
    harness static void test (int x) {
        ABC a = new ABC(x);
        a.handler.onEvent();
        assert ABC.x == x + 1;
        a.handler.onEvent();
        assert ABC.x == x + 2;
    }
}

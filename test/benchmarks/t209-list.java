interface IObserver {
    public void notify();
}

class Subject {
    ArrayList<IObserver> obs;

    public Subject () {
        obs = new ArrayList<IObserver>();
    }

    public void register(IObserver o) {
        obs.add(o);
    }

    public void unregister(IObserver o) {
        obs.remove(o);
    }

    void onEvent() {
        if (obs.isEmpty())
          return;

        for (IObserver o : obs) {
            o.notify();
        }
    }
}

class Observer implements IObserver {
    boolean notified;

    public Observer () {
        notified = false;
    }

    public void notify () {
        notified = true;
    }

    public boolean isNotified () {
        return notified;
    }

    public void reset () {
        notified = false;
    }
}

class Test {
    harness static void test () {
        Subject s = new Subject();
        // Observer o1 = new Observer();
        Observer o2 = new Observer();
        // Observer o3 = new Observer();
        // s.register(o1);
        s.register(o2);
        // s.register(o3);

        // s.onEvent();
        // assert o1.isNotified();
        // assert o2.isNotified();
        // assert o3.isNotified();

        // o1.reset();
        // o2.reset();
        // o3.reset();
        // assert ! o1.isNotified();
        // assert ! o2.isNotified();
        // assert ! o3.isNotified();

        s.unregister(o2);
        s.onEvent();
        // assert o1.isNotified();
        assert ! o2.isNotified();
        // assert o3.isNotified();
    }
}

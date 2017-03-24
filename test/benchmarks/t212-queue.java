class Task {
    static int count = 0;
    static int nonce () {
        count = count + 1;
        return count;
    }

    public int hash;

    public Task() {
        hash = Task.nonce();
    }
}

class TaskQueue {
    Queue<Task> q;

    public TaskQueue() {
        q = new AbstractQueue<Task>();
    }

    public void add(Task t) {
        q.add(t);
    }

    public Task remove() {
        if (!isEmpty()) {
            return q.remove();
        }
        return null;
    }

    public boolean isEmpty() {
        return q.isEmpty();
    }
}

class Test {
    harness static void test () {
        TaskQueue tq = new TaskQueue();
        Task t = new Task();
        assert t.hash == 1;
        tq.add(t);
        t = new Task();
        assert t.hash == 2;
        tq.add(t);
        t = new Task();
        assert t.hash == 3;
        tq.add(t);

        t = tq.remove();
        assert t.hash == 1;
        t = tq.remove();
        assert t.hash == 2;
        t = tq.remove();
        assert t.hash == 3;

        assert tq.isEmpty();
    }
}

class Task { }
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
class AbstractQueue_remove {
    harness void m() {
	TaskQueue tq = new TaskQueue();
	Task t = new Task();
	
	tq.add(t);
	t = tq.remove();
    }
}

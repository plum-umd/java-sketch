package java.util;

public class HashSet<E> implements Set<E> {
    E[] set;
    int capacity;
    int size;

    static final int INITIAL_CAPACITY;

    public HashSet() {
        this.INITIAL_CAPACITY = 16;
        set = new E[INITIAL_CAPACITY];
        size = 0;
        capacity = INITIAL_CAPACITY;
    }

    public HashSet(List<E> es) {
        this.INITIAL_CAPACITY = 16;
        set = new E[INITIAL_CAPACITY];
        size = 0;
        capacity = INITIAL_CAPACITY;
        for(Iterator<E> it = es.iterator(); it.hasNext();) {
            this.add(it.next());
        }
    }

    private void resize(int newSize) {
        E[] oldSet = set;
        E[] newSet = new E[newSize];

        for (int i = 0; i < capacity; i++) {
            if (oldSet[i] != null) {
                int oldHash = hashMod(oldSet[i], capacity);
                int newHash = hashMod(oldSet[i], newSize);
                newSet[newHash] = oldSet[oldHash];
            }
        }

        this.set = newSet;
        this.capacity = newSize;
    }

    private int hashMod(Object o, int mod) {
        int hash = o.hashCode() % mod;
        if (hash < 0) {
            hash += mod;
        }
        return hash;
    }

    public boolean contains(Object o) {
        int hash = hashMod(o, capacity);
        E entry = set[hash];

        return entry != null && o.equals(entry);
    }

    public boolean add(E e) {
        int hash = hashMod(e, capacity);
        E entry = set[hash];

        while (entry != null && !e.equals(entry)) {
            resize(capacity + 4);
            hash = hashMod(e, capacity);
            entry = set[hash];
        }

        if (entry != null) {
            return false;
        } else {
            set[hash] = e;
            size++;
            return true;
        }
    }

    public boolean remove(Object o) {
        int hash = hashMod(o, capacity);

        if (set[hash] != null) {
            set[hash] = null;
            size--;
            return true;
        }

        return false;
    }

    public void clear() {
        set = new E[INITIAL_CAPACITY];
        size = 0;
        capacity = INITIAL_CAPACITY;
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }
}

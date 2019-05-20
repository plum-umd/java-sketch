package java.util;

private class LLNode<E>{
    public E value = null;
    public LLNode<E> prev = null;
    public LLNode<E> next = null;
}


public class LinkedList<E> implements List<E>{
    private LLNode<E> head = null;
    private LLNode<E> last = null;
    private int size = 0;

    public LinkedList() {
    }

    public LinkedList(List<E> es) {
        this.addAll(es);
    }

    public void addAll(List<E> a2) {
	int len = a2.size();
	for (int i = 0; i < len; i++) {
	    this.add(a2.get(i));
	}
    }
    
    public void sort(Object c) {

    }

    public <E> void add(int index, E e) {
        if(index < 0 || index > this.size) {
            throw new IndexOutOfBoundsException();
        } else if (index == this.size) {
            add(e);
        } else {
            LLNode<E> elem = getNode(index);
            LLNode<E> node = new LLNode<E>();
            node.value = e;
            node.prev = elem.prev;
            node.prev.next = node;
            node.next = elem;
            node.next.prev = node;
            this.size++;
        }
    }

    public <E> boolean add(E e) {
        LLNode<E> node = new LLNode<E>();
        node.value = e;
        if(this.last != null) {
            node.prev = this.last;
            node.prev.next = node;
            this.last = node;
        } else {
            this.head = node;
            this.last = node;
        }

        this.size++;
        return true;
    }

    public void clear() {
        this.head = null;
        this.last = null;
        this.size = 0;
    }

    public boolean contains(Object o) {
        return indexOf(o) >= 0;
    }

    public E get(int index) {
        if (index < 0 || index >= size) {
            return null;
        }

        LLNode<E> node = getNode(index);
        return node.value;
    }

    public int indexOf(Object o) {
        LLNode<E> cur = head;
        int i = 0;
        for (i = 0; i < size; i++) {
            if(o == null) {
                if(cur.value == null)
                    return i;
            } else {
                if(o.equals(cur.value))
                    return i;
            }
            cur = cur.next;
        }
        return -1;
    }

    public E remove(int index) {
        if (index < 0 || index >= size) {
            return null;
        }

        LLNode<E> node = getNode(index);
        removeNode(node);
        return node.value;
    }

    public boolean remove(Object o) {
        LLNode<E> cur = head;
        int i = 0;
        for (i = 0; i < size; i++) {
            if(o == null) {
                if(cur.value == null) {
                    removeNode(cur);
                    return true;
                }
            } else {
                if(o.equals(cur.value)) {
                    removeNode(cur);
                    return true;
                }
            }
            cur = cur.next;
        }

        return false;
    }

    public <E> E set (int index, E element) {
        if (index < 0 || index >= size) {
            return null;
        }

        LLNode<E> node = getNode(index);
        E oldElement = node.value;
        node.value = element;
        return oldElement;
    }

    public int size() {
        return size;
    }

    public int length() {
        return size();
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public E[] toArray() {
        Object[] arr = new Object[size];
        LLNode<E> cur = head;
        int i = 0;
        for (i = 0; i < size; i++) {
            arr[i] = cur.value;
            cur = cur.next;
        }

        return arr;
    }

    public List<E> subList(int fromIndex, int toIndex) {
        subListRangeCheck(fromIndex, toIndex, size);
        LLNode<E> cur = getNode(fromIndex);
        LinkedList<E> a = new LinkedList<E>();
        for (int i = 0; i < toIndex-fromIndex; i++) {
            a.add(cur.value);
            cur = cur.next;
        }
        return a;
    }

    static void subListRangeCheck(int fromIndex, int toIndex, int size) {
        assert fromIndex >= 0;
        assert toIndex <= size;
        assert fromIndex < toIndex;
    }

    private LLNode<E> getNode(int n) {
        LLNode<E> cur = head;
        int i = 0;
        for (i = 0; i < n; i++)
            cur = cur.next;
        assert cur != null;
        return cur;
    }

    private void removeNode(LLNode<E> node) {
        if(node.prev != null) {
            node.prev.next = node.next;
        } else {
            this.head = node.next;
        }
        if(node.next != null) {
            node.next.prev = node.prev;
        } else {
            this.last = node.prev;
        }
        this.size--;
    }
}


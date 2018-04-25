public interface Deque <E> {
    public boolean add(E e);
    public void addFirst(E e);
    public void addLast(E e);
    public boolean contains(Object o);
    public E getFirst();
    public E getLast();
    public E peek();
    public E peekFirst();
    public E peekLast();
    public E remove();
    public boolean remove(Object o);
    public E removeFirst();
    public E removeLast();
    public int size();
    public boolean isEmpty();
}

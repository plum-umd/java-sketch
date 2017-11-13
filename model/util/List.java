package java.util;

public interface List <E> {
  public <E> boolean add(E e);
  public boolean isEmpty();
  public E get(int index);
  public void remove(Object e);
  public boolean remove(int index);
}

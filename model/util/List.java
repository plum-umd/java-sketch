package java.util;

public interface List <E> {
  public boolean add(Object e);
  public boolean isEmpty();
  public E get(int index);
  public void remove(Object e);
  public boolean remove(int index);
}

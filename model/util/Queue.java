package java.util;

public interface Queue<E>{
  public boolean add(E e);
  public boolean isEmpty();

  public E element();
  public E peek();
  public E poll();
  public E remove();

  public void clear();
}

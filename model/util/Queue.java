package java.util;

public interface Queue<E>{
  public <E> boolean add(E e);
  public E element();
  public E peek();
  public E poll();
  public E remove();
}

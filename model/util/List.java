package java.util;

import java.lang.Iterable;

public interface List <E> extends Iterable<E> {
  public <E> boolean add(E e);
  public boolean isEmpty();
  public E get(int index);
  public E remove(int index);
  public boolean remove(Object e);
  public <E> E set (int index, E element);
  public int size();
}

package java.util;

@JSketchStdLib
public interface Iterator <E> {
    public boolean hasNext();
    public E next();
    public void remove();
}

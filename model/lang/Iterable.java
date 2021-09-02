package java.lang;

import java.util.Iterator;

@JSketchStdLib
public interface Iterable <T> {
    public Iterator<T> iterator();
}

@axiomClass
public class PrintStream {
    @constructor
    @adt
    PrintStream PrintStream(FileOutputStream fos);

    @adt
    void close();

    @adt
    void print(String s);
}

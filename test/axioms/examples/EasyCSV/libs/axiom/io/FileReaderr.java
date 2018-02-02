@axiomClass
public class FileReaderr {
    @adt
    @constructor
    FileReaderr FileReaderr(String path);

    @adt
    public char read();

    @adt
    public void close();
}

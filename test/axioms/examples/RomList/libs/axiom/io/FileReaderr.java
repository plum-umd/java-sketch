// @axiomClass
// public class FileReaderr {
//     @adt
//     @constructor
//     FileReaderr FileReaderr(String path);

//     @adt
//     public char read();

//     @adt
//     public void close();
// }

public class FileReaderr {
    String data;

    public FileReaderr(String path) {
	this.data = path;
    }

    public FileReaderr(File f) {
    	this.data = f.path;
    }
    
    public int len(String [] strs) {
	return strs.length;
    }
    
    public char read() { return 0; }

    public void close() { }
}

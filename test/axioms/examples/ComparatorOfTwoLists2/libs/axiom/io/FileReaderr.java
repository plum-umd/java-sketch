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
    String path;
    String[] data;
    
    public FileReaderr(String path) {
	this.path = path;
	this.data = path.split("\n");
    }

    public int len(String [] strs) {
	return strs.length;
    }

    public String get(int i) {
	if (i < data.length) {
	    return this.data[i];
	}
	return null;
    }
    
    public char read() { return 0; }

    public void close() { }
}

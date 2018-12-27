public class FileReaderr {
    String path;
    String data;
    int position;
    
    public FileReaderr(String path) {
	this.path = path;
	this.position = 0;
	this.data = path;
    }

    public char read() {
	if (position < data.length()) {
	    char c = data.charAt(position);
	    position++;
	    return c;
	}
	return -1;
    }

    public void close() {

    }
}

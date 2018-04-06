public class File {
    String fname;
    int size;
    File(String fname) {
	this.fname = fname;
	this.size = 0;
    }
    int size() { return this.size; }

    public boolean exists() {
	return true;
    }

    public String getName() {
	return this.fname;
    }

    public String getParent() {
	return "PATH";
    }
}

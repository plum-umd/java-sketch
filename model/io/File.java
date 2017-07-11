public class File {
    String fname;
    int size;
    File(String fname) {
	this.fname = fname;
	this.size = 0;
    }
    int size() { return this.size; }
}

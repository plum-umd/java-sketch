public class File {
    String path;
    String[] data;
    
    public File(String path) {
	this.path = path;
	this.data = path.split("\n");
    }

    public String get(int i) {
	if (i < data.length) {
	    return this.data[i];
	}
	return null;
    }
    
    public boolean exists() { return true; }

    public String getName() { return this.path; }

    public String getParent() { return "PATH"; }
}

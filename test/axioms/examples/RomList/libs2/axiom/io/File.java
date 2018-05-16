public class File {
    String path;

    public File(String path) {
	this.path = path;
    }

    public boolean exists() { return true; }

    public String getName() { return this.path; }

    public String getParent() { return "PATH"; }
}

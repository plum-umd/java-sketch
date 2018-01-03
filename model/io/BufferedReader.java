public class BufferedReader {
    FileReaderr reader;
    
    public BufferedReader(FileReaderr reader) {
	this.reader = reader;
    }

    public String readLine() {
	char c = this.reader.read();
	StringBuilder sb = new StringBuilder();
	while (c != '\n') {
	    sb.append(c);
	    c = this.reader.read();
	}
	return sb.toString();
    }
}

class FileReaderr {
    File file;
    FileReaderr(File file) { this.file = file; }

    boolean ready() { return file.size() > 0; }
    int read() { return 0; }
    void close() { }
}

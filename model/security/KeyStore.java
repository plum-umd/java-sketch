public class KeyStore {
    public String instance;

    public KeyStore(String instance) {
	this.instance = instance;
    }

    public static KeyStore getInstance(String instance) {
	return new KeyStore(instance);
    }

    public void load(Object o) {

    }

    // public Entry getEntry(String alias, Object o) {
    // 	return new Entry();
    // }
    
    // public class Entry {
    // 	public Entry() {

    // 	}
    // }

    // public class SecretKeyEntry extends Entry{
    // 	public SecretKeyEntry() {

    // 	}
    // }

    // public class PrivateKeyEntry extends Entry{
    // 	public PrivateKeyEntry() {

    // 	}
    // }
}

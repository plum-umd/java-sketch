public class Properties {

    HashMap<String, String> map;
    
    public Properties() {
	map = new HashMap<>();
    }

    public void setProperty(String key, String value) {
	map.put(key, value);
    }
}

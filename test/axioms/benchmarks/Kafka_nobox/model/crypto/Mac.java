public class Mac {
    public Mac() {

    }

    public static Mac getInstance(String type) {
	return new Mac();
    }

    public void init(SecretKeySpec key) {

    }

    public byte[] doFinal(byte[] text) {
	return text;
    }
}

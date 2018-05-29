public class Utils {
    public static Cipher getCipherInstance(String trans, Properties props) {
	return new Cipher(trans);
    }
}

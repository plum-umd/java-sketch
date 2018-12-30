public class Utils {
    public static Cipher getCipherInstance(String trans, Properties props) {
	return Cipher.getInstance(trans, trans);
	// return new Cipher(trans);
    }
}

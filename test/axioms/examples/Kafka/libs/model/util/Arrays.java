public class Arrays {

    public static byte[] copyOf(byte[] in, int len) {
	byte[] n = new byte[len];

	for (int i = 0; i < len; i++) {
	    if (i >= in.length) {
		n[i] = 0;
	    } else {
		n[i] = in[i];
	    }
	}
	return n;
    }

    // public static boolean equals(byte[] b1, byte[] b2) {    
    public static boolean arraysEquals(byte[] b1, byte[] b2) {
	if (b1.length == b2.length) {
	    for (int i = 0; i < b1.length; i++) {
		if (b1[i] != b2[i]) return false;
	    }
	} else {
	    return false;
	}
	return true;
    }
}

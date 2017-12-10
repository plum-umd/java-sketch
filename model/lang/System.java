public class System {

    public static void arraycopy(byte[] src, int srcPos, byte[] dst, int dstPos, int length) {
	for (int i = srcPos; i < srcPos+length; i++) {
	    dst[dstPos+i] = src[i];
	}
    }
}

@rewriteClass
// @autoBox
class Cipher {

    public static Cipher getInstance(String type, String prov) {
    	return new Cipher(type, prov);
    }

    @alg
    @constructor
    Cipher Cipher(String t, String p);

    // @alg
    // void getInstance(String type);
    
    // @alg
    // void init(int mode, Object k, Object iv);

    // @alg
    // void init(int mode, SecretKeySpec s);

    @alg
    // void init(int mode, SecretKeySpec s, AlgorithmParameterSpec a);
    Object init(int mode, SecretKeySpec s, AlgorithmParameterSpec a);

    @alg
    // @boxedArg(1)
    // @boxedRet
    // int update(byte[] data, int a, int len, byte[] out, int b);
    int update(Object data, int a, int len, byte[] out, int b);
    
    @alg
    @boxedRet
    Object doFinal(Object data);

    @alg
    // int doFinale(byte[] data, int a, int b, byte[] out, int c);
    int doFinale(Object data, int a, int b, byte[] out, int c);
    
    @alg
    @pure
    int getOutputSize(int len);

    rewrite Object getOutputSize(Object init!(Cipher c1, SecretKeySpec k1, AlgorithmParameterSpec a1), int l) {
    	return l;
    }
    
    // rewrite Object update(Cipher c1, byte[] data, int a, int len, byte[] out, int b) {
    rewrite Object update(Cipher c1, Object data, int a, int len, byte[] out, int b) {
    	return 0;
    }

    // rewrite Object doFinale(Object update!(Cipher c1, byte[] d1, int a1, int l1, byte[] o1, int b1), byte[] d2, int a2, int b2, byte[] o2, int c2) {
    rewrite Object doFinale(Object update!(Cipher c1, byte[] d1, int a1, int l1, byte[] o1, int b1), Object d2, int a2, int b2, byte[] o2, int c2) {
    	return l1;
    }

    rewrite Object doFinal(
    			   Object doFinale!(
    					    Object update!(
    							   Object init!(Cipher c1, int m1, SecretKeySpec k1, AlgorithmParameterSpec i1),
    							   byte[] d1, int a1,
    							   int l1, byte[] o1, int b1),
    					    byte[] d2, int a2, int b2, byte[] o2,
    					    int c2),
    			   Object doFinal(
    					  Object doFinale!(
    							   Object update!(Object init!(Cipher c3, int m3, SecretKeySpec k3, AlgorithmParameterSpec i3), byte[] d3, int a3, int l3, byte[] o3, int b3), byte[] d4, int a4, int b4, byte[] o4, int c4), Object text)) {
    	return k1.equals(k3) ? text : null;
    }
    
    // rewrite Object doFinal(Object init!(Cipher c1, int m1, SecretKeySpec k1, AlgorithmParameterSpec a1), Object doFinal(Object init!(Cipher c2, int m2, SecretKeySpec k2, AlgorithmParameterSpec a2), Object t)) {
    // 	return k1.equals(k2) ? ((m1 == 2 && m2 == 1) ? t : null) : null;
    // }

    // rewrite Object doFinal(Object init!(Object getInstance!(Cipher c1, String type1), int m1, Object k1), Object doFinal(Object init!(Cipher c2, int m2, Object k2), Object t)) {
    // 	return k1.equals(k2) ? t : null;
    // }
    
}

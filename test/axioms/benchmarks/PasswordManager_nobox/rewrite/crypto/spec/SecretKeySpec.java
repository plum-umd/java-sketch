@rewriteClass
public class SecretKeySpec implements Key {
    @alg
    @pure
    byte[] getEncoded();

    rewrite Object getEncoded(Object SecretKeySpec()) {
    	return new byte[16];
    }
    
}

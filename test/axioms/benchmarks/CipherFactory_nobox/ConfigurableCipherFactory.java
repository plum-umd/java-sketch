package com.cl.xlp.core.impl.common.crypt;

/**
 * Cipher factory that allows configurable algorithm and padding.
 */
public class ConfigurableCipherFactory extends DefaultCipherFactory {
    
    public void setAlgorithm(String algorithm) {
        this.algorithm = algorithm;
    }

    public void setPadding(String padding) {
        this.padding = padding;
    }

}

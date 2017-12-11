package com.nucypher.kafka.cipher;

import com.nucypher.kafka.Constants;
import com.nucypher.kafka.errors.CommonException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Factory for {@link ICipher}
 */
public class CipherFactory {

    private static final Logger LOGGER = LoggerFactory.getLogger(CipherFactory.class);

    /**
     * Cipher provider
     */
    public enum CipherProvider {
        /**
         * BouncyCastle provider
         */
        BOUNCY_CASTLE,
        /**
         * OpenSSL provider by JNI
         */
        OPENSSL
    }

    /**
     * Get {@link ICipher} instance
     *
     * @param provider       {@link CipherProvider}
     * @param transformation transformation
     * @return instance of {@link ICipher}
     */
    public static ICipher getCipher(CipherProvider provider,
                                    String transformation) {
        LOGGER.info("Creating cipher using provider '{}' and transformation '{}'",
                provider, transformation);
        String algorithm = transformation.split("/")[0];
        switch (provider) {
            case BOUNCY_CASTLE:
                return new JCECipher(
                        Constants.BOUNCY_CASTLE_PROVIDER_NAME,
                        algorithm,
                        transformation);
            case OPENSSL:
                return new OpenSSLCipher(algorithm, transformation);
            default:
                throw new CommonException("Unknown provider '%s'", provider);
        }
    }

}

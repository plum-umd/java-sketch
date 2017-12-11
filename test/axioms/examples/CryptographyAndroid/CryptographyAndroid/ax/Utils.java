package com.cheetah.cryptography;

import android.support.annotation.NonNull;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;

public final class Utils {

    private Utils() {
    }

    /**
     * Simple constant-time equality of two byte arrays. Used for security to avoid timing attacks.
     *
     * @param a
     * @param b
     * @return true iff the arrays are exactly equal.
     */
    public static boolean constantTimeEq(byte[] a, byte[] b) {
        if (a.length != b.length) {
            return false;
        }
        int result = 0;
        for (int i = 0; i < a.length; i++) {
            result |= a[i] ^ b[i];
        }
        return result == 0;
    }

    public static byte[] bytesConcat(byte[] iv, byte[] cipherText) {
        byte[] combined = new byte[iv.length + cipherText.length];
        System.arraycopy(iv, 0, combined, 0, iv.length);
        System.arraycopy(cipherText, 0, combined, iv.length, cipherText.length);
        return combined;
    }

    /**
     * @param cipher       the algorithm
     * @param plainData    UTF-8 bytes
     * @param bufferLength
     * @return
     * @throws IllegalBlockSizeException
     * @throws BadPaddingException
     */
    public static byte[] decodeWithBuffer(@NonNull Cipher cipher, @NonNull byte[] plainData, int bufferLength) throws IllegalBlockSizeException, BadPaddingException {

        byte[] scrambled;
        byte[] toReturn = new byte[0];
        byte[] buffer = new byte[(plainData.length > bufferLength ? bufferLength : plainData.length)];

        for (int i = 0; i < plainData.length; i++) {
            if ((i > 0) && (i % bufferLength == 0)) {
                scrambled = cipher.doFinal(buffer);
                toReturn = append(toReturn, scrambled);
                int newLength = bufferLength;

                if (i + bufferLength > plainData.length) {
                    newLength = plainData.length - i;
                }
                buffer = new byte[newLength];
            }
            buffer[i % bufferLength] = plainData[i];
        }

        scrambled = cipher.doFinal(buffer);
        toReturn = append(toReturn, scrambled);
        return toReturn;
    }

    public static byte[] append(byte[] prefix, byte[] suffix) {
        byte[] toReturn = new byte[prefix.length + suffix.length];
        for (int i = 0; i < prefix.length; i++) {
            toReturn[i] = prefix[i];
        }
        for (int i = 0; i < suffix.length; i++) {
            toReturn[i + prefix.length] = suffix[i];
        }
        return toReturn;
    }
}

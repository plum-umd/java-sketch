package com.cheetah.cryptography;

import android.util.Base64;

/**
 * Created by fahadHAlotaibi on 12/31/16.
 */

public final class CipherTextContainer {
    private final byte[] cipherText;
    private final byte[] iv;
    private final byte[] mac;

    private CipherTextContainer() {
        cipherText = new byte[0];
        iv = new byte[0];
        mac = new byte[0];
    }

    public CipherTextContainer(byte[] ct, byte[] iv, byte[] mc) {
        this.cipherText = new byte[ct.length];
        System.arraycopy(ct, 0, this.cipherText, 0, ct.length);
        this.iv = new byte[iv.length];
        System.arraycopy(iv, 0, this.iv, 0, iv.length);
        this.mac = new byte[mc.length];
        System.arraycopy(mc, 0, mac, 0, mc.length);
    }

    public CipherTextContainer(String base64CipherText) {
        String[] civArray = base64CipherText.split(":");
        if (civArray.length != 3) {
            throw new IllegalArgumentException("Cannot parse cipherText");
        } else {
            iv = Base64.decode(civArray[0], Base64.NO_WRAP);
            mac = Base64.decode(civArray[1], Base64.NO_WRAP);
            cipherText = Base64.decode(civArray[2], Base64.NO_WRAP);
        }
    }

    public byte[] getCipherText() {
        return cipherText;
    }

    public byte[] getIv() {
        return iv;
    }

    public byte[] getMac() {
        return mac;
    }

    @Override
    public String toString() {
        String ivString = Base64.encodeToString(iv, Base64.NO_WRAP);
        String macString = Base64.encodeToString(mac, Base64.NO_WRAP);
        String cipherTextString = Base64.encodeToString(cipherText, Base64.NO_WRAP);
        return ivString + ":" + macString + ":" + cipherTextString;
    }
}

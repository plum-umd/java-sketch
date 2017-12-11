package com.cheetah.cryptography;

import android.annotation.TargetApi;
import android.content.Context;
import android.os.Build;
import android.preference.PreferenceManager;
import android.security.KeyPairGeneratorSpec;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.support.annotation.RequiresApi;
import android.util.Base64;
import android.widget.Toast;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.security.GeneralSecurityException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.UnrecoverableEntryException;
import java.security.cert.CertificateException;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.concurrent.atomic.AtomicBoolean;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.Mac;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.security.auth.x500.X500Principal;

import static com.cheetah.cryptography.Utils.decodeWithBuffer;


public final class CryptographyManager {

    private static final String PREF_PUBLIC_KEY = "prefrencePublicKey";
    public static final String ENCODE_FORMAT = "UTF-8";
    private static final AtomicBoolean prngFixed = new AtomicBoolean(false);
    private Context context;

    private CryptographyManager() {
    }

    public CryptographyManager(Context context) {
        this.context = context;
    }

    /**
     * this method will generate a SecretKey and store it in the key store under the keystoreAlias.
     * you need the keystoreAlias to get it the Secret key from keyStore
     *
     * @param keystoreAlias
     * @return
     * @throws NoSuchProviderException
     * @throws NoSuchAlgorithmException
     * @throws InvalidAlgorithmParameterException
     * @throws KeyStoreException
     * @throws IOException
     * @throws CertificateException
     */
    @RequiresApi(api = Build.VERSION_CODES.M)
    private SecretKey generateAESKey(String keystoreAlias) throws NoSuchProviderException, NoSuchAlgorithmException, InvalidAlgorithmParameterException, KeyStoreException, IOException, CertificateException {
        fixPrng();
        KeyGenerator keyGen = KeyGenerator.getInstance(AES.CIPHER, KeyStoreConstants.PROVIDER);
        KeyGenParameterSpec.Builder builder = new KeyGenParameterSpec.Builder(keystoreAlias,
                KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_CBC)
                .setKeySize(AES.KEY_LENGTH_BITS)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_PKCS7);
        keyGen.init(builder.build());
        return keyGen.generateKey();
    }

    @TargetApi(Build.VERSION_CODES.KITKAT)
    @SuppressWarnings("deprecation")
    private KeyPair generateRSAKey(String keystoreAlias) throws NoSuchProviderException, NoSuchAlgorithmException, InvalidAlgorithmParameterException {
        fixPrng();
        Calendar start = new GregorianCalendar();
        Calendar end = new GregorianCalendar();
        end.add(Calendar.YEAR, 10);
        KeyPairGeneratorSpec spec =
                new KeyPairGeneratorSpec.Builder(context)
                        .setAlias(keystoreAlias)
                        .setSubject(new X500Principal("CN=" + keystoreAlias))
                        .setSerialNumber(BigInteger.valueOf(1337))
                        .setStartDate(start.getTime())
                        .setEndDate(end.getTime())
                        .setKeySize(RSA.KEY_LENGTH_BITS)
                        .build();
        KeyPairGenerator kpGenerator = KeyPairGenerator.getInstance(RSA.CIPHER, KeyStoreConstants.PROVIDER);
        kpGenerator.initialize(spec);
        KeyPair keyPair = kpGenerator.generateKeyPair();
        storePublicKey(keyPair.getPublic());
        return keyPair;
    }

    /**
     * @param plainText     the text to encrypt
     * @param keystoreAlias alias of the entry in which the generated key will appear in
     *                      Android KeyStore. Must not be empty.
     * @return the encrypted text
     */
    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public String encrypt(String plainText, String keystoreAlias) throws KeyStoreException, CertificateException, NoSuchAlgorithmException, IOException, NoSuchProviderException, InvalidAlgorithmParameterException, IllegalBlockSizeException, InvalidKeyException, BadPaddingException, NoSuchPaddingException, UnrecoverableEntryException {

        KeyStore keyStore = KeyStore.getInstance(KeyStoreConstants.PROVIDER);
        keyStore.load(null);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            SecretKey encryptionKey = null;
            SecretKey integrityKey = null;

            if (keyStore.containsAlias(keystoreAlias)) {
                KeyStore.Entry encryptionKeyEntry = keyStore.getEntry(keystoreAlias, null);
                if (encryptionKeyEntry instanceof KeyStore.SecretKeyEntry)
                    encryptionKey = ((KeyStore.SecretKeyEntry) encryptionKeyEntry).getSecretKey();
            }

            if (encryptionKey == null)
                encryptionKey = generateAESKey(keystoreAlias);

            if (keyStore.containsAlias(HMAC.INTEGRITY_SUFFIX + keystoreAlias)) {
                KeyStore.Entry integrityKeyEntry = keyStore.getEntry(HMAC.INTEGRITY_SUFFIX + keystoreAlias, null);
                if (integrityKeyEntry instanceof KeyStore.SecretKeyEntry)
                    integrityKey = ((KeyStore.SecretKeyEntry) integrityKeyEntry).getSecretKey();
            }

            if (integrityKey == null)
                integrityKey = generateAESIntegrityKey(keystoreAlias);

            return encryptPlaintText(encryptionKey, integrityKey, plainText.getBytes(ENCODE_FORMAT)).toString();
        } else {
            KeyPair keyPair = null;

            if (keyStore.containsAlias(keystoreAlias)) {
                KeyStore.Entry encryptionKeyEntry = keyStore.getEntry(keystoreAlias, null);
                if (encryptionKeyEntry instanceof KeyStore.PrivateKeyEntry) {
                    PublicKey publicKey = getPublicKey();
                    if (publicKey != null)
                        keyPair = new KeyPair(publicKey, ((KeyStore.PrivateKeyEntry) encryptionKeyEntry).getPrivateKey());
                }
            }

            if (keyPair == null)
                keyPair = generateRSAKey(keystoreAlias);

            return encryptPlainText(keyPair.getPublic(), plainText);
        }
    }

    private PublicKey getPublicKey() {
        try {
            String publicKeyString = PreferenceManager.getDefaultSharedPreferences(context).getString(PREF_PUBLIC_KEY, null);
            byte[] publicKeyBytes = Base64.decode(publicKeyString, Base64.NO_WRAP);
            X509EncodedKeySpec x509KeySpec = new X509EncodedKeySpec(publicKeyBytes);
            KeyFactory keyFact = null;
            try {
                Cipher cipher = Cipher.getInstance(RSA.CIPHER_TRANSFORMATION);
                keyFact = KeyFactory.getInstance(RSA.CIPHER, cipher.getProvider());
            } catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
            }

            try {
                return keyFact.generatePublic(x509KeySpec);
            } catch (InvalidKeySpecException e) {
                e.printStackTrace();
            }
            return null;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    private void storePublicKey(PublicKey publicKey) {
        try {
            byte[] publicKeyBytes = publicKey.getEncoded();
            String publicKeyString = Base64.encodeToString(publicKeyBytes, Base64.NO_WRAP);
            PreferenceManager.getDefaultSharedPreferences(context).edit().putString(PREF_PUBLIC_KEY, publicKeyString).apply();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    private SecretKey generateAESIntegrityKey(String keystoreAlias) throws NoSuchProviderException, NoSuchAlgorithmException, InvalidAlgorithmParameterException, InvalidKeyException {
        KeyGenerator keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_HMAC_SHA256, KeyStoreConstants.PROVIDER);
        keyGenerator.init(new KeyGenParameterSpec.Builder(HMAC.INTEGRITY_SUFFIX + keystoreAlias, KeyProperties.PURPOSE_SIGN).build());
        return keyGenerator.generateKey();
    }

    /**
     * This method encrypt the plain text using AES
     *
     * @param secretKey the key will be used to encrypt the plaintext
     * @param plaintext the plaint text in UTF-8 format
     * @return
     */
    @RequiresApi(api = Build.VERSION_CODES.M)
    private CipherTextContainer encryptPlaintText(SecretKey secretKey, SecretKey integrityKey, byte[] plaintext) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        Cipher aesCipherForEncryption = Cipher.getInstance(AES.CIPHER_TRANSFORMATION);
        aesCipherForEncryption.init(Cipher.ENCRYPT_MODE, secretKey);
        Mac hMac = Mac.getInstance(HMAC.CIPHER);
        hMac.init(integrityKey);
        byte[] byteCipherText = aesCipherForEncryption.doFinal(plaintext);
        byte[] iv = aesCipherForEncryption.getIV();
        byte[] ivAndCipherText = Utils.bytesConcat(iv, byteCipherText);
        byte[] mac = hMac.doFinal(ivAndCipherText);
        return new CipherTextContainer(byteCipherText, iv, mac);
    }

    private String encryptPlainText(PublicKey publicKey, String plaintext) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, IOException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance(RSA.CIPHER_TRANSFORMATION);
        Toast.makeText(context, cipher.getProvider().getName(), Toast.LENGTH_SHORT).show();
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        byte[] cipherText = decodeWithBuffer(cipher, plaintext.getBytes(ENCODE_FORMAT), RSA.KEY_LENGTH_BITS / 8 - 11);
        return Base64.encodeToString(cipherText, Base64.DEFAULT);
    }

    public String decrypt(String cipherText, String keyStoreAlias) throws GeneralSecurityException, IOException {
        KeyStore keyStore = KeyStore.getInstance(KeyStoreConstants.PROVIDER);
        keyStore.load(null);

        KeyStore.Entry entry = keyStore.getEntry(keyStoreAlias, null);

        if (entry == null)
            throw new IllegalArgumentException("no key found in the keyStore, double check the keyStoreAlias");

        KeyStore.Entry integrityKey = keyStore.getEntry(HMAC.INTEGRITY_SUFFIX + keyStoreAlias, null);

        if (entry instanceof KeyStore.SecretKeyEntry && integrityKey instanceof KeyStore.SecretKeyEntry) {
            CipherTextContainer cipherTextContainer = new CipherTextContainer(cipherText);
            return decryptCipherText(((KeyStore.SecretKeyEntry) entry).getSecretKey(), ((KeyStore.SecretKeyEntry) integrityKey).getSecretKey(), cipherTextContainer);
        } else if (entry instanceof KeyStore.PrivateKeyEntry) {
            return decryptCipherText(cipherText, ((KeyStore.PrivateKeyEntry) entry).getPrivateKey());
        } else
            throw new IllegalArgumentException("i found entry key which is not instanceof SecretKey or PrivateKeyEntry ");
    }

    /**
     * this method decrypts the cipher text using AES algorithm
     *
     * @param cipherTextContainer the cipher text to decrypt and the iv
     * @return the encrypted text
     */
    private String decryptCipherText(SecretKey decryptionKey, SecretKey integrityKey, CipherTextContainer cipherTextContainer) throws GeneralSecurityException, UnsupportedEncodingException {
        Mac hMac = Mac.getInstance(HMAC.CIPHER);
        hMac.init(integrityKey);

        byte[] ivAndCipher = Utils.bytesConcat(cipherTextContainer.getIv(), cipherTextContainer.getCipherText());
        byte[] computedMac = hMac.doFinal(ivAndCipher);
        if (Utils.constantTimeEq(computedMac, cipherTextContainer.getMac())) {
            Cipher aesCipherForDecryption = Cipher.getInstance(AES.CIPHER_TRANSFORMATION);
            aesCipherForDecryption.init(Cipher.DECRYPT_MODE, decryptionKey, new IvParameterSpec(cipherTextContainer.getIv()));
            return new String(aesCipherForDecryption.doFinal(cipherTextContainer.getCipherText()), ENCODE_FORMAT);
        } else
            throw new GeneralSecurityException("MAC stored in civ does not match computed MAC.");
    }

    private String decryptCipherText(String cipherText, PrivateKey privateKey) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, UnsupportedEncodingException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipherDecrypt = Cipher.getInstance(RSA.CIPHER_TRANSFORMATION);
        cipherDecrypt.init(Cipher.DECRYPT_MODE, privateKey);
        byte[] plainText = decodeWithBuffer(cipherDecrypt, Base64.decode(cipherText, Base64.DEFAULT), RSA.KEY_LENGTH_BITS / 8);
        return new String(plainText, ENCODE_FORMAT);
    }

    /**
     * Ensures that the PRNG is fixed. Should be used before generating any keys.
     * Will only run once, and every subsequent call should return immediately.
     */
    private void fixPrng() {
        if (!prngFixed.get()) {
            synchronized (PrngFixes.class) {
                if (!prngFixed.get()) {
                    PrngFixes.apply();
                    prngFixed.set(true);
                }
            }
        }
    }

    public static final class AES {
        public static final String CIPHER_TRANSFORMATION = "AES/CBC/PKCS7Padding";
        public static final String CIPHER = "AES";
        public static final int KEY_LENGTH_BITS = 128;
    }

    public static final class RSA {
        public static final String CIPHER_TRANSFORMATION = "RSA/ECB/PKCS1Padding";
        public static final String CIPHER = "RSA";
        public static final int KEY_LENGTH_BITS = 1024;
    }

    public static final class HMAC {
        public static final String INTEGRITY_SUFFIX = BuildConfig.APPLICATION_ID + "INTEGRITY_SUFFIX";
        public static final String CIPHER = "HmacSHA256";
    }


    public static final class KeyStoreConstants {
        public static final String PROVIDER = "AndroidKeyStore";

        public static final class Alias {

        }

    }
}

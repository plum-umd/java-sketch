package com.cl.xlp.core.impl.common.crypt;

import org.junit.Assert;
import org.junit.Test;

public class ConfigurableCipherFactoryTest {

    @Test
    public void testConfiguration() {
        ConfigurableCipherFactory f = new ConfigurableCipherFactory();
        f.setAlgorithm("alg");
        f.setPadding("pad");
        Assert.assertEquals("alg", f.getAlgorithm());
        Assert.assertEquals("pad", f.getPadding());
    }

}

class test {

    harness void mn() {
	for (int TID = 0; TID < 15; TID++) {
	    if (TID==0) t0();
	    else if (TID==1) t1();
	    else if (TID==2) t2();
	    else if (TID==3) t3();
	    else if (TID==4) t4();
	    else if (TID==5) t5();
	    else if (TID==6) t6();
	    else if (TID==7) t7();
	    else if (TID==8) t8();
	    else if (TID==9) t9();
	    else if (TID==10) t10();
	    else if (TID==11) t11();
	    else if (TID==12) t12();
	    else if (TID==13) t13();
	    else if (TID==14) t14();
	}
    }
    
    // get(put([],x,y), x) == y
    void t0() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();

	h.put(x,y);
	Object gxpx = h.get(x);

	assert gxpx.equals(y);
    }

    // get(put(put([],x,y), w, z), x) = y
    void t1() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object w = new Object();	
	Object z = new Object();

	h.put(x,y);
	h.put(w,z);

	Object gxpxw = h.get(x);

	assert gxpxw.equals(y);
    }

    // get(put(put([],x,y), x, z), x) = z
    void t2() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);
	h.put(x,z);

	Object gxpxx = h.get(x);

	assert gxpxx.equals(z);
    }

    // get(put(put(put(put(put([],x,y), w, z), a, b), c, d), e, f), x) = y
    void t3() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object w = new Object();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();
	Object a = new Object();
	Object b = new Object();
	Object c = new Object();
	Object d = new Object();
	Object e = new Object();
	Object f = new Object();

	h.put(x,y);
	h.put(w,z);
	h.put(a,b);
	h.put(c,d);
	h.put(e,f);
	
	Object gxpxwace = h.get(x);

	assert gxpxwace.equals(y);
    }

    // get(remove(put(put([],x,y), x, z), x), x) = null
    void t4() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);
	h.put(x,z);
	h.remove(x);

	Object gxrxpxx = h.get(x);

	assert gxrxpxx == null;
    }

    // get(put(remove(put([],x,y), x), x, z), x) = z
    void t5() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);
	h.remove(x);
	h.put(x,z);
	
	Object gxpxrxpx = h.get(x);

	assert gxpxrxpx.equals(z);
    }

    // containsKey(put([],x,y), x) == true
    void t6() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();

	h.put(x,y);

	assert h.containsKey(x);
    }

    // containsKey(put(put(put(put(put([],x,y), w, z), a, b), c, d), e, f), x) = 
    //   true
    void t7() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object w = new Object();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();
	Object a = new Object();
	Object b = new Object();
	Object c = new Object();
	Object d = new Object();
	Object e = new Object();
	Object f = new Object();

	h.put(x,y);
	h.put(w,z);
	h.put(a,b);
	h.put(c,d);
	h.put(e,f);

	assert h.containsKey(x);
    }

    // containsKey(put([],x,y), z) == false
    void t8() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);

	assert !h.containsKey(z);
    }

    // containsKey(remove(put(put([],x,y), x, z), x), x) = false
    void t9() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);
	h.put(x,z);
	h.remove(x);

	assert !h.containsKey(x);
    }

    // containsKey(put(remove(put([],x,y), x), x, z), x) = true
    void t10() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);
	h.remove(x);
	h.put(x,z);

	assert h.containsKey(x);
    }

    // containsValue(put([],x,y), y) == true
    void t11() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();

	h.put(x,y);

	assert h.containsValue(y);
    }

    // containsValue(put(put(put(put(put([],x,y),w, z), a, b), c, d), e, f), y) =
    //   true
    void t12() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object w = new Object();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();
	Object a = new Object();
	Object b = new Object();
	Object c = new Object();
	Object d = new Object();
	Object e = new Object();
	Object f = new Object();

	h.put(x,y);
	h.put(w,z);
	h.put(a,b);
	h.put(c,d);
	h.put(e,f);

	assert h.containsValue(y);
    }

    // containsValue(put(put([],x,y), x, z), y) = false
    void t13() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);
	h.put(x,z);
	
	assert !h.containsValue(y);
    }

    // containsValue(remove(put(put([],x,y), w, z), x), y) = false
    void t14() {
	HashMap_NoHash h = new HashMap_NoHash<Object, Object>();
	Object w = new Object();
	Object x = new Object();
	Object y = new Object();
	Object z = new Object();

	h.put(x,y);
	h.put(w,z);
	h.remove(x);

	assert !h.containsValue(y);	
    }

}

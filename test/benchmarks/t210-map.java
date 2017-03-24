interface IService {
    public String getName();
    public void request();
}

class WindowManager implements IService {
    private WindowManager() {
        name = "WindowManager";
    }

    static WindowManager m;

    public static WindowManager getInstance() {
        if (m == null) {
            m = new WindowManager();
        }
        return m;
    }

    String name;

    public String getName() {
        return name;
    }

    public void request() {
    }
}

class LocationManager implements IService {
    private LocationManager() {
        name = "LocationManager";
    }

    static LocationManager m;

    public static LocationManager getInstance() {
        if (m == null) {
            m = new LocationManager();
        }
        return m;
    }

    String name;

    public String getName() {
        return name;
    }

    public void request() {
    }
}

class ServiceManager {
    Map<String, IService> services;

    public ServiceManager() {
        services = new HashMap_Simple<String, IService>(); // will be replaced with TreeMap<K,V>
    }

    public void register(String name, IService srv) {
        services.put(name, srv);
    }

    public IService lookup(String name) {
        if (services.containsKey(name)) {
            return services.get(name);
        }
        return null;
    }

    public void reset() {
        services.clear();
    }
}

class Test {
    harness static void test () {
        ServiceManager sm = new ServiceManager();

        WindowManager wm = WindowManager.getInstance();
        sm.register(wm.getName(), wm);

        // LocationManager lm = LocationManager.getInstance();
        // sm.register(lm.getName(), lm);

        // WindowManager wm2 = sm.lookup(wm.getName());
        // assert wm2 != null;
        // assert wm2 == wm;

        // LocationManager lm2 = sm.lookup(lm.getName());
        // assert lm2 != null;
        // assert lm2 == lm;

        // sm.reset();
        // wm2 = sm.lookup(wm.getName());
        // assert wm2 == null;
        // lm2 = sm.lookup(lm.getName());
        // assert lm2 == null;
    }
}

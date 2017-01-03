class A {
}

class B extends A {
    int z = 0;
    
}

class Cast {
    public static void main(String[] args) {
	A a = new A();
	int x = ((B)a).z;
    }
}

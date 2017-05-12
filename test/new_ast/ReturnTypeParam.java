class ReturnTypeParam<T> {
    ReturnTypeParam rt;
    ReturnTypeParam<T> get() { return this.rt; }
    ReturnTypeParam<T> set(ReturnTypeParam<T> rt) { return this.rt; }

    harness void mn() {
	ReturnTypeParam rt = new ReturnTypeParam();
	rt.set(rt);
	ReturnTypeParam rt1 = get();
    }
}


class Array {
    harness static void main() {
	int[] a0 = new int[5];
	assert a0.length == 5;

	double[] a1;
	a1 = new double[10];
	assert a1[0] == 0.0;

	int[] a2 = {1, 2};
	assert a2[0] == 1 && a2[1] == 2;

	int[] a3 = new int[] {0};
	assert a3[0] == 0;
	
	int[] a4;
	a4 = new int[] {0};
	assert a4[0] == 0;

	int[] a5 = {1,2,3,4,5};
	assert list_sum(a5) == 15;
    }
    int list_sum(int[] lst) {
	int sum = 0;
	for (int i = 0; i < lst.length; ++i) {
	    sum += lst[i];
	}
	return sum;
    }
}

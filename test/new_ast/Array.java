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
    }
}

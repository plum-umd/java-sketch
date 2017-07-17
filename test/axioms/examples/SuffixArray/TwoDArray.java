public class TwoDArray {

    int[] arr;
    int N, M;
    
    public TwoDArray(int n, int m) {
	N = n;
	M = m;
	arr = new int[n*m];
    }

    public void set(int i, int j, int val) {
    	arr[(i*M)+j] = val;
    }

    public int get(int i, int j) {
    	return arr[(i*M)+j];
    }

    public void setRow(int i, int[] row) {
	int count = 0;
	for (int j=i*M; j<(i*M)+M; j++) {
	    arr[j] = row[count];
	    count ++;
	}
    }

    public int[] getRow(int i) {
	int count = 0;
	int[] row = new int[M];
	for (int j=i*M; j<(i*M)+M; j++) {
	    row[count] = arr[j];
	    count ++;
	}
	return row;
    }
}

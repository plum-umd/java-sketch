public class A implements Runnable {
    class Point {
        double x, y;
    }

    private Point getStart(double x, Point p1, Point p2) {
        if (x < p1.x) {
            return p1;
        }
	else if (x > p2.x) {
            return null;
        }
	else {
            Point ret = new Point();
            return ret;
        }
    }
}

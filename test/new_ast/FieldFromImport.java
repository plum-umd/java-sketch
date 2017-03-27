import java.awt.geom.Point2D;

class FieldFromImport extends Point2D.Double {
    class Inner { }
    harness void main() {
	double a = this.x;
    }
}

@axiomClass
public class OtherObjects {
    @adt
    String get(String s);

    axiom Object get(Object get!(OtherObjects o, String s1), String s2) {
	return s1;
    }
}

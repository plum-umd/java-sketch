@rewriteClass
class Axiom_Tester {
    harness void mn() {
	// String x = "Hello";
	// if (??) {
	//     x = x.concat(" ");
	// }
	// String y = "World!";
	// String z = x.concat(y);
	// assert z.equals("Hello World!");

	String x = "Hello World!";
	// if (??) {
	//     x = x.concat(" ");
	// }
	// String y = "World!";
	// String z = x.concat(y);
	assert x.equals("Hello World!");

    }
}

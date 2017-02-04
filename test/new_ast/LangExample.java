// This is an example with the modelled lang files
// To run with model: ./jsk test/new_ast/LangExample.java model/
class LangExample {
    harness void main() {
	// This turns into the string constructor defined in String.java
	// Without the model that constructor won't exist so this will fail.
	// Strings are hardcoded to use the modelled constructor (java_sk/translator.py:536).
	String s = "Hello, world!";
	// This uses the charAt method in String.java
	assert s.charAt(1) == 'e';
    }
}

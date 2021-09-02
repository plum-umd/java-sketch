package java.lang;

@JSketchStdLib
public class Character {
    // public static final int MIN_RADIX = 2;
    // public static final int MAX_RADIX = 36;
    // // Unicode problems
    // // public static final char MIN_VALUE = '\u0000';
    // // public static final char MAX_VALUE = '\uFFFF';
    // public static final byte UNASSIGNED = 0;
    // public static final byte UPPERCASE_LETTER = 1;
    // public static final byte LOWERCASE_LETTER = 2;
    // public static final byte TITLECASE_LETTER = 3;
    // public static final byte MODIFIER_LETTER = 4;
    // public static final byte OTHER_LETTER = 5;
    // public static final byte NON_SPACING_MARK = 6;
    // public static final byte ENCLOSING_MARK = 7;
    // public static final byte COMBINING_SPACING_MARK = 8;
    // public static final byte DECIMAL_DIGIT_NUMBER        = 9;
    // public static final byte LETTER_NUMBER = 10;
    // public static final byte OTHER_NUMBER = 11;
    // public static final byte SPACE_SEPARATOR = 12;
    // public static final byte LINE_SEPARATOR = 13;
    // public static final byte PARAGRAPH_SEPARATOR = 14;
    // public static final byte CONTROL = 15;
    // public static final byte FORMAT = 16;
    // public static final byte PRIVATE_USE = 18;
    // public static final byte SURROGATE = 19;
    // public static final byte DASH_PUNCTUATION = 20;
    // public static final byte START_PUNCTUATION = 21;
    // public static final byte END_PUNCTUATION = 22;
    // public static final byte CONNECTOR_PUNCTUATION = 23;
    // public static final byte OTHER_PUNCTUATION = 24;
    // public static final byte MATH_SYMBOL = 25;
    // public static final byte CURRENCY_SYMBOL = 26;
    // public static final byte MODIFIER_SYMBOL = 27;
    // public static final byte OTHER_SYMBOL = 28;
    // public static final byte FINAL_QUOTE_PUNCTUATION = 30;
    // // Unicode problems
    // // static final int ERROR = 0xFFFFFFFF;
    // public static final byte DIRECTIONALITY_UNDEFINED = -1;
    // public static final byte DIRECTIONALITY_LEFT_TO_RIGHT = 0;
    // public static final byte DIRECTIONALITY_RIGHT_TO_LEFT = 1;
    // public static final byte DIRECTIONALITY_RIGHT_TO_LEFT_ARABIC = 2;
    // public static final byte DIRECTIONALITY_EUROPEAN_NUMBER = 3;
    // public static final byte DIRECTIONALITY_EUROPEAN_NUMBER_SEPARATOR = 4;
    // public static final byte DIRECTIONALITY_EUROPEAN_NUMBER_TERMINATOR = 5;
    // public static final byte DIRECTIONALITY_ARABIC_NUMBER = 6;
    // public static final byte DIRECTIONALITY_COMMON_NUMBER_SEPARATOR = 7;
    // public static final byte DIRECTIONALITY_NONSPACING_MARK = 8;
    // public static final byte DIRECTIONALITY_BOUNDARY_NEUTRAL = 9;
    // public static final byte DIRECTIONALITY_PARAGRAPH_SEPARATOR = 10;
    // public static final byte DIRECTIONALITY_SEGMENT_SEPARATOR = 11;
    // public static final byte DIRECTIONALITY_WHITESPACE = 12;
    // public static final byte DIRECTIONALITY_OTHER_NEUTRALS = 13;
    // public static final byte DIRECTIONALITY_LEFT_TO_RIGHT_EMBEDDING = 14;
    // public static final byte DIRECTIONALITY_LEFT_TO_RIGHT_OVERRIDE = 15;
    // public static final byte DIRECTIONALITY_RIGHT_TO_LEFT_EMBEDDING = 16;
    // public static final byte DIRECTIONALITY_RIGHT_TO_LEFT_OVERRIDE = 17;
    // public static final byte DIRECTIONALITY_POP_DIRECTIONAL_FORMAT = 18;

    // Sketch isn't into unicode 
    // public static final char MIN_HIGH_SURROGATE = '\uD800';
    // public static final char MAX_HIGH_SURROGATE = '\uDBFF';
    // public static final char MIN_LOW_SURROGATE  = '\uDC00';
    // public static final char MAX_LOW_SURROGATE  = '\uDFFF';
    // public static final char MIN_SURROGATE = '\uD800';
    // public static final char MAX_SURROGATE = '\uDFFF';
    // public static final char MIN_SURROGATE = MIN_HIGH_SURROGATE;
    // public static final char MAX_SURROGATE = MAX_LOW_SURROGATE;
    // Sketch isn't into hex values
    // public static final int MIN_SUPPLEMENTARY_CODE_POINT = 0x010000;
    // public static final int MIN_CODE_POINT = 0x000000;
    // public static final int MAX_CODE_POINT = 0X10FFFF;

    char value;

    public Character(char value) {
	this.value = value;
    }

    public char charValue() {
	return value;
    }

    public boolean equals(Object obj) {
    	if (obj instanceof Character) {
    	    return value == ((Character)obj).charValue();
    	}
    	return false;
    }
}


package easycsv;

/**
 * Created by Dan Geabunea on 3/21/2015.
 */
class CodeAssertion {

    /**
     * Check if the provided expression is valid.
     * @param expression the logical condition/argument to check for validity
     * @throws EasyCsvAssertionRuntimeException in case the expression is invalid
     */
    public static void verifyThat(boolean expression){
        if(!expression){
            throw new EasyCsvAssertionRuntimeException();
        }
    }

    /**
     * Check if the provided expression is valid.
     * @param expression the logical condition/argument to check for validity
     * @param message the custom error message that will be appended to the runtime error
     * @throws EasyCsvAssertionRuntimeException in case the expression is invalid
     */
    public static void verifyThat(boolean expression, String message){
        if(!expression){
            throw new EasyCsvAssertionRuntimeException(message);
        }
    }
}

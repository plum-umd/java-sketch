package easycsv.test;

import easycsv.CsvColumn;
import easycsv.EasyCsvConversionException;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.time.LocalDate;

import static org.junit.Assert.*;

/**
 * Created by Dan Geabunea on 3/21/2015.
 */
// @RunWith(JUnitParamsRunner.class)
public class CsvColumnTest {

    @Test
    public void the_getIntValue_method_when_column_is_integer_should_return_correct_result(){
        //arrange
        String someIntValue = "20";
        CsvColumn someIntCsvColumn = new CsvColumn(someIntValue);

        //act
        int result = someIntCsvColumn.getInteger();

        //assert
        // assertEquals(20, result);
	assert 20 == result;
    }

    // @Test(expected = EasyCsvConversionException.class)
    // public void the_getIntValue_method_when_column_not_integer_should_throw(){
    //     //arrange
    //     String someValue = "fd";
    //     CsvColumn someCsvColumn = new CsvColumn(someValue);

    //     //act
    //     someCsvColumn.getInteger();
    // }

    // @Test
    // public void the_getDoubleValue_method_when_column_is_double_should_return_correct_result(){
    //     //arrange
    //     String someDoubleValue = "20.2";
    //     CsvColumn someDoubleCsvColumn = new CsvColumn(someDoubleValue);

    //     //act
    //     double result = someDoubleCsvColumn.getDouble();

    //     //assert
    //     // assertEquals(20.2, result, 0.0000001);
    // 	assert (20.2 - result) > -0.0000001 && (20.2-result) < 0.0000001;
    // }

    // @Test(expected = EasyCsvConversionException.class)
    // public void the_getDoubleValue_method_when_column_no_double_should_throw(){
    //     //arrange
    //     String someValue = "fd";
    //     CsvColumn someCsvColumn = new CsvColumn(someValue);

    //     //act
    //     someCsvColumn.getDouble();
    // }

    // @Test
    // @Parameters({
    //         "true,false",
    //         "True,False",
    //         "TRUE, FALSE",
    //         "t,f",
    //         "T,F",
    //         "yes,no",
    //         "Yes,No",
    //         "YES,NO",
    //         "Y,N",
    //         "y,n",
    //         "1,0"})
    public void the_getBooleanValue_method_when_column_can_be_converted_to_boolean_should_return_correct_result(String trueValue, String falseValue){
        //arrange
        CsvColumn columnWithTrueResult = new CsvColumn(trueValue);
        CsvColumn columnWithFalseResult = new CsvColumn(falseValue);

        //act
        boolean resultThatShouldBeTrue = columnWithTrueResult.getBoolean();
        boolean resultThatShouldBeFalse = columnWithFalseResult.getBoolean();

        //assert
        // assertTrue(resultThatShouldBeTrue);
        // assertFalse(resultThatShouldBeFalse);

	assert resultThatShouldBeTrue;
	assert resultThatShouldBeFalse;	
    }

    // @Test
    // @Parameters({
    //         "2014-01-01,yyyy-MM-DD"
    // })
    // public void the_getDateValue_method_when_column_is_date_and_format_is_valid_should_return_correct_result(String date, String dateFormat){
    //     //arrange
    //     CsvColumn csvColumn = new CsvColumn(date);

    //     //act
    //     LocalDate result = csvColumn.getDate(dateFormat);

    //     //assert
    //     assertEquals(2014, result.getYear());
    //     assertEquals(1, result.getMonthValue());
    //     assertEquals(1, result.getDayOfMonth());
    // }
}

package easycsv.test;

import easycsv.CsvColumn;
import easycsv.CsvRow;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

/**
 * Created by Dan Geabunea on 3/24/15.
 */
public class CsvRowTest {

    public static void runTests() {
	the_constructor_with_column_values_argument_should_build_row();
	the_constructor_with_variable_columns_argument_should_build_row();
	the_constructor_with_column_list_argument_should_build_row();
    }
    
    @Test
    public static void the_constructor_with_column_values_argument_should_build_row(){
        //arrange
        String someValue = "1";
        String anotherValue = "value";

        //act
        CsvRow someRow = new CsvRow(someValue, anotherValue);

        //assert
        // assertEquals(2, someRow.getNumberOfColumns());
        // assertFalse(someRow.isEmpty());
        // assertTrue(someRow.getColumnAtIndex(0).getColumnValue().equals(someValue));
        // assertTrue(someRow.getColumnAtIndex(1).getColumnValue().equals(anotherValue));
	assert 2 == someRow.getNumberOfColumns();
	assert !(someRow.isEmpty());
	CsvColumn c1 = someRow.getColumnAtIndex(0);
	String i1 = c1.getColumnValue();
	assert i1.equals(someValue);
	CsvColumn c2 = someRow.getColumnAtIndex(1);
	String i2 = c2.getColumnValue();
	assert i2.equals(anotherValue);
    }

    @Test
    public static void the_constructor_with_variable_columns_argument_should_build_row(){
        //arrange
        String someValue = "1";
        String anotherValue = "value";
        CsvColumn someColumn = new CsvColumn(someValue);
        CsvColumn anotherColumn = new CsvColumn(anotherValue);

        //act
        CsvRow someRow = new CsvRow(someColumn, anotherColumn);

        //assert
        // assertEquals(2, someRow.getNumberOfColumns());
        // assertFalse(someRow.isEmpty());
        // assertTrue(someRow.getColumnAtIndex(0).getColumnValue().equals(someValue));
        // assertTrue(someRow.getColumnAtIndex(1).getColumnValue().equals(anotherValue));
    	assert 2 == someRow.getNumberOfColumns();
    	assert !(someRow.isEmpty());
    	CsvColumn c1 = someRow.getColumnAtIndex(0);
    	String i1 = c1.getColumnValue();
    	assert i1.equals(someValue);
    	CsvColumn c2 = someRow.getColumnAtIndex(1);
    	String i2 = c2.getColumnValue();
    	assert i2.equals(anotherValue);
    }

    @Test
    public static void the_constructor_with_column_list_argument_should_build_row(){
        //arrange
        String someValue = "1";
        String anotherValue = "value";
        CsvColumn someColumn = new CsvColumn(someValue);
        CsvColumn anotherColumn = new CsvColumn(anotherValue);
        // List<CsvColumn> rowColumns = new ArrayList<>(Arrays.asList(someColumn,anotherColumn));
        ArrayList<CsvColumn> rowColumns = new ArrayList<>();
    	rowColumns.add(someColumn);
    	rowColumns.add(anotherColumn);

        //act
        CsvRow someRow = new CsvRow(rowColumns);

        //assert
        // assertEquals(2, someRow.getNumberOfColumns());
        // assertFalse(someRow.isEmpty());
        // assertTrue(someRow.getColumnAtIndex(0).getColumnValue().equals(someValue));
        // assertTrue(someRow.getColumnAtIndex(1).getColumnValue().equals(anotherValue));
    	assert 2 == someRow.getNumberOfColumns();
    	assert !(someRow.isEmpty());
    	CsvColumn c1 = someRow.getColumnAtIndex(0);
    	String i1 = c1.getColumnValue();
    	assert i1.equals(someValue);
    	CsvColumn c2 = someRow.getColumnAtIndex(1);
    	String i2 = c2.getColumnValue();
    	assert i2.equals(anotherValue);
    }
}

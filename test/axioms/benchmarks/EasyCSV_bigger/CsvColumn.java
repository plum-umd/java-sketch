package easycsv;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import static easycsv.CodeAssertion.verifyThat;

/**
 * Created by Dan Geabunea on 3/21/2015.
 */
public class CsvColumn {
    private String columnValue;

    /*
    Instantiates a CsvColumn with no columnValue (null)
     */
    public CsvColumn(){
    }

    public CsvColumn(String value) {
        this.columnValue = value;
    }

    public CsvColumn(int intValue){
        this.columnValue = Integer.toString(intValue);
    }

    // public CsvColumn(double doubleValue){
    //     this.columnValue = Double.toString(doubleValue);
    // }

    public CsvColumn(boolean booleanValue){
        this.columnValue = Boolean.toString(booleanValue);
    }

    // public CsvColumn(LocalDate dateValue){
    //     this.columnValue = dateValue.toString();
    // }

    public boolean hasValue(){
        return columnValue == null;
    }

    public String getColumnValue() {
        return columnValue;
    }

    public int getInteger(){
        // verifyThat(columnValue != null, EasyCsvErrorMessages.nullValue(columnValue));
        // try {
            int parsedValue = Integer.parseInt(columnValue);
            return parsedValue;
        // }
        // catch (NumberFormatException e){
        //     throw new EasyCsvConversionException(EasyCsvErrorMessages.integerConversion(columnValue));
        // }
    }

    // public double getDouble(){
    //     // verifyThat(columnValue != null, EasyCsvErrorMessages.nullValue(columnValue));
    //     // try {
    //         double parsedValue = Double.parseDouble(columnValue);
    //         return parsedValue;
    //     // }
    //     // catch (NumberFormatException e){
    //     //     throw new EasyCsvConversionException(EasyCsvErrorMessages.doubleConversion(columnValue));
    //     // }
    // }

    public boolean getBoolean(){
        // verifyThat(columnValue != null, EasyCsvErrorMessages.nullValue(columnValue));

        //check for true values
        if(columnValue.equalsIgnoreCase("true") ||
                columnValue.equalsIgnoreCase("t") ||
                columnValue.equalsIgnoreCase("yes") ||
                columnValue.equalsIgnoreCase("y") ||
                columnValue.equals("1")){
            return true;
        }

        //check for true values
        if(columnValue.equalsIgnoreCase("false") ||
                columnValue.equalsIgnoreCase("f") ||
                columnValue.equalsIgnoreCase("no") ||
                columnValue.equalsIgnoreCase("n") ||
                columnValue.equals("0")){
            return false;
        }

        // throw new EasyCsvConversionException(EasyCsvErrorMessages.booleanConversion(columnValue));
	return false;
    }

    // public LocalDate getDate(String dateFormat){
    //     // verifyThat(columnValue != null, EasyCsvErrorMessages.nullValue(columnValue));

    //     // try {
    //         DateTimeFormatter formatter = DateTimeFormatter.ofPattern(dateFormat);
    //         LocalDate dateTime = LocalDate.parse(columnValue, formatter);
    //         return dateTime;
    //     // } catch (Exception e) {
    //     //     throw new EasyCsvConversionException(EasyCsvErrorMessages.dateConversion(columnValue, dateFormat));
    //     // }
    // }

}

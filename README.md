csvExport
=========

Converting csv file from QuickPALM or ThunderSTORM to [ViSP](http://www.nature.com/nmeth/journal/v10/n8/full/nmeth.2566.html?WT.ec_id=NMETH-201308)

## Usage

### After selected input file, you can double click on the header of the list to add columns to "Selected Columns"

Usage for visualization in ViSP:
* choose your file(csv or xls)
* for 3d visualization, fill the corresponding column number to make sure you have the column and order as "x y z intensity frame", then click "Export"
* for 2d visualization, fill the corresponding column number to make sure you have the column and order as "x y intensity frame", then click "Export"

Usage for Matlab:
* choose your file
* fill the column number you want to export to "Selected Columns"
* put "," in "Output Delimiter";
    click Export, specify the extension as ".csv"
    and use csvread() to load data.
    data = csvread(FILE_PATH);

Example settings for convert from Vutar particle csv file format to thunderSTROM format:
* Input delimiter:  ,
* Selected Column:   4, 16, 17, 18, 7
* Output delimiter:  ,
* Header:    "frame","x [nm]","y [nm]","z [nm]","intensity [photon]"


### Parameters
* Input Delimiter: the delimiter used to separate columns, for csv and xls file, this parameter will change automatically.
* Selected Columns: the column number and order you want to have in the target file
* Output Delimiter: the delimiter of exported file used to separate columns, eg. "\t" for xls file and "," for csv file.
* Header: the output header, you can edit if you want to change for the output.

###

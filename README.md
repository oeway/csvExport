csvExport
=========

Converting csv file from QuickPALM or ThunderSTORM to [ViSP](http://www.nature.com/nmeth/journal/v10/n8/full/nmeth.2566.html?WT.ec_id=NMETH-201308)

## Usage
Usage for visualization in ViSP:
* choose your file(csv or xls)
* for 3d visualization, just click "Export".
* for 2d visualization, put "x,y,intensity,frame" in "Export Format" and click "Export".

Usage for Matlab:
* choose your file
* put "," in "Export Delimiter";
    click Export, specify the extension as ".csv"
    and use csvread() to load data.
    data = csvread(FILE_PATH);

### Parameters
* Import Delimiter: the delimiter used to separate columns, for csv and xls file, this parameter will change automatically.
* Export Format: the column name and order you want to have in the exported file
* Export Delimiter: the delimiter of exported file used to separate columns, use "\t" for xls file and "," for csv file.

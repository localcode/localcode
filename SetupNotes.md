# Configuration for Local Code

---

## Development Configuration

1. Install gVIM (or MacVim)
2. Install Inconsolata font
3. Install git
4. Fork the dotfiles repo into the HOME folder
    * Using the installed git command line program command line program, type `cd ~` and enter
    * then, `git clone git@github.com:bengolder/dotfiles.git .` and enter (the `.` at the end is important)
    * then, `git remote add upstream git://github.com/bengolder/dotfiles.git` and enter
    * then, `git fetch upstream` and enter

---

## Dependencies for Local Code

1. Install OSGeo4W
2. Install PostgreSQL 9.0 32-bit (psycopg2 currently needs postgres 9.0 and postgis must be 32-bit) 
3. Install Python 2.6 if not already installed (32-bit)
4. This step may not be necessary
    > Install psycopg2 for python 2.6.x and postgreSQL 9.x
    > 	This ran into an error: "Unable to find vcvarsall.bat"
    > 	It was suggested to either install MS Visual Studio C++ express (because it simply lacks a compiler)
    > 	Or to install an earlier version of psycopg2
5. Add things to the PATH system environmental variable

    * Python (`C:\Program Files (x86)\Python26`)
    * PostgreSQL (`C:\Program Files (x86)\PostgreSQL\9.0\bin`) - Necessary for running psql commands
    * OSGeo4W Tools (`C:\OSGeo4W\bin`) - Necessary for using ogr2ogr and gdal tools
    * The above collectively: `;C:\Program Files (x86)\Python26;C:\Program Files (x86)\PostgreSQL\8.4\bin;C:\OSGeo4W\bin`
    * resulting Path:  `C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Program Files (x86)\QuickTime\QTSystem;C:\arcgis\arcexe9x\bin;C:\Program Files (x86)\Microsoft SQL Server\100\Tools\Binn\;C:\Program Files\Microsoft SQL Server\100\Tools\Binn\;C:\Program Files\Microsoft SQL Server\100\DTS\Binn\;C:\Program Files (x86)\QuickTime\QTSystem\;C:\Program Files (x86)\Python26;C:\Program Files (x86)\PostgreSQL\8.4\bin;C:\OSGeo4W\bin`

6. Create a new Envrionmental variable called `GDAL_DATA` that points to where the csv files for epsg codes are stored. In this case it was `C:\OSGeo4W\apps\gdal-17\share\gdal`
6. Install python packages in `C:\Program Files (x86)\Python26\Lib\site-packages`

---

## To Load GIS Data into PostgreSQL 

`shpPopulate` has a variety of functions for dealing with this. It depends on the above dependencies being installed.

1. Open PgAdmin (should have been installed with PostgreSQL) and make a new database for certain project (assuming you want to keep the GIS data separate).
    * right click on 'Databases', and say 'New Database'.
    * use `template_postgis` at the template for the database
2. Check out your shapefiles and prepare them for loading:
    * Determine a directory that holds all your shapefiles (they can be nested, but find the top directory)
    * use the `getShpFiles` function in `shpPopulate` to print a list of all your shapefiles
    * ensure that all the shapefiles have names that dont include really crazy characters, such as '&' or '%', etc.
    * use `getUniqueProjections` in `shpPopulate` to view of list of the different projections (or lack thereof) present in your shapefiles.
    * Use proj2srid.org and spatialreference.org to look up the epsg codes for each projection and assemble them into an srid list
    * order the epsg codes in your srid list to correspond with the order of the unqiue projections read by `getUniqueProjections`.
7. Use the `shpToPostgreSQL` function to print out the commands to load all the files using the SRID list.
8. check the commands to ensure that nothing is worng (for example, does it connect to the correct database?)
8. run the commands, and wait a long time for the data to load.


---

## To Start Importing Data into Rhino

1. install [setuptools](http://pypi.python.org/pypi/setuptools#downloads)
2. add the setup tools script directory to the PATH system variable `C:\Program Files (x86)\Python26\Scripts`
3. download the [psycopg2 installer](http://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg) for win32, python 2.6
4. run the psycopg2 installer as administrator
5. run cmd.exe as administrator
6. Install pip:
    * `$ curl -O https://github.com/pypa/pip/raw/master/contrib/get-pip.py`
    * `$ python get-pip.py`
7. Install geojson:
    * `$ pip install geojson`





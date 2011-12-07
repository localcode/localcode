## Local Code ##

- - -

<!--This is a repository of scripts being used on the [Local Code Project](http://nicholas.demonchaux.com) which is currently in residency at the [Autodesk Idea Studio](http://usa.autodesk.com/ideastudio).-->
<!--These scripts are new, messy, and in development. Feel free to browse them, but don't expect them to work well or safely on your computer.  -->



####So far the scripts include:  
- shpPopulate.py: used for loading a large quantity of shapefiles into a PostGIS/PostgreSQL database.
- db.py: some scripts for running queries and retrieving gis data
- sql.py: scripts for composing specific sql queries.
- mayascripts.py: a set of functions used in Autodesk Maya to retrieve and render animations of gis data based on SQL queries

### Development

1. Install a good text editor or IDE
2. Get a GitHub account.
2. [Install Git and set it up.](http://help.github.com/win-set-up-git/)

### Installation and Setup - Windows

The software for local code is a set of Python modules. These modules use other
tools to manage gis data and build 3d models. Here is an overview of the steps:

1. Install the database and GIS tools.
2. Make sure that the GIS tools can be found by Python
3. Install the code libraries.

After that, you can begin loading and exporting data.

#### 1. Install the spatial database, GIS tools, and Python.

1. Install PostgreSQL (9.0.4) (when it asks, just tell it to listen on the
   defalt port)

    [download link](http://www.enterprisedb.com/products-services-training/pgdownload#windows)
    Select the Win x86-32 version.
    When it asks, just tell it to listen on the default port.
    After the installation is finished, it will open StackBuilder, which you
    can use to install PostGIS.

2. Install PostGIS 

    In StackBuilder, install PostGIS (listed under 'Spatial Extensions').

4. Install OSGeo4W (Use the Express Desktop Install)

    [download link](http://download.osgeo.org/osgeo4w/osgeo4w-setup.exe)
    During Installation, select the 'Express Desktop Install'.

4. Install Python

    [download link](http://www.python.org/download/releases/2.6.6/)
    Select the 'Windows x86 MSI 2.6.6' version.

#### 2. Make sure that the GIS tools can be found by python

<!--I could make a python script to do this-->
1. Make sure that the PostgreSQL/bin folder (where PostgreSQL keeps it's
   scripts) is on the PATH.

    There are two ways to do this.
    In the start menu, type 'env' and select 'Edit System Environmental Variables'    
    or go to Control Panel and find 'Edit System Environmental Variables'
    Scroll down the list of variables, and find the one labeled 'Path'
    Edit 'Path' by copying and pasting its contents into a text document.
    At the end of path, add the folder names for:

    * the PostgreSQL/bin folder (probably `C:\Program Files (x86)\PostgreSQL\9.0\bin`)
    * the Python folder (probably `C:\Python26` or `C:\Program Files (x86)\Python26`)
    * the Python/Scripts folder
    * the OSGeo4W folder that contains `ogr2ogr` and `ogrinfo` (probably `C:\OSGeo4W\bin`)

<!--check on command line to make sure that things work-->

#### 3. Install the code libraries

1. Install setuptools [download link](http://pypi.python.org/pypi/setuptools#files) (setuptools-0.6c11.win32-py2.6.exe)
2. Install pip.

    Open 'cmd' by right-clicking on it and selecting 'Run As Administrator'.
    Enter the following commands:

    ```bash
    curl -O https://github.com/pypa/pip/raw/master/contrib/get-pip.py
    python get-pip.py
    ```

3. Use the following commands, while still running 'cmd' as administrator, to
   install Python libraries.

    ```bash
    pip install psycopg2
    ```

    For using the Excel configuration utilities if you want to configure your
    shapefiles with a spreadsheet.

    ```bash
    pip install xlwt
    pip install xlrd
    ```

    And if you want to use these tools for 3d geometry.

    <!--This is a likely place for failure.-->
    ```bash
    pip install numpy
    pip install scipy
    ```


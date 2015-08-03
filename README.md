# Process_EMC_XML_Files
Python modules to process XML files pulled from EMC Arrays

This module is written using Python 3.4 and uses the XMLNS package to crawl the XML.  The format of the telemetry uses namespaces and therefore requires this package.

ProcessTelemetryFile.py
  The VNX products produce a Telemetry.xml file which contains configuration and usage information typically pulled through sp collects.   This module allows the SE or anyone with access to the XML file to create a report without the SP collect.
  
  Usage:  create a directory with to place the XML file(s) in.  The default is C:\Telemetryfiles\ (windows) or 
  /TelemetryFiles/  off root (Unix/MAC).  The code is present to detect the OS and select the right default.   As of 8/3/2015 I have not tested non-windows execution so if there are any issues please contact me at parrir@gmail.com.
  
  My recomendation is to use the default directory.
  
  Once the files are in this directory run the module and it will parse each file and create a filename.txt output for each input file.
  
ProcessSymmDIscover.py
  Currently under construction.
  

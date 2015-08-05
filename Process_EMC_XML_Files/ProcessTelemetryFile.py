from sys import platform as _platform
from xml.etree import ElementTree as ET
import os 
import sys

namespaces = {"UEM_FILE":"http://emc.com/uem/schemas/EMC_UEM_Telemetry_File_Schema", 
      "ARRAY_REG":"http://emc.com/uem/schemas/ArrayRegistrationSchema", 
      "CLAR":"http://emc.com/uem/schemas/Common_CLARiiON_schema", 
      "FILEMETADATA":"http://emc.com/uem/schemas/Common_CLARiiON_Type_schema", 
      "SAN":"http://emc.com/uem/schemas/Common_CLARiiON_SAN_schema"}

#
#  Build file header
#
separater = ("--------------------------------------------------------------------\n")
def print_header(arg1, arg2, arg3):
    f.write(separater)
    f.write(line2)
    f.write(separater)
    return None

# Placeholder code for disk type conversion
def convert_disk(dsktype):
    if dsktype.text == "1":
        disktype = "EFD"
    elif dsktype.text == "2":
        disktype = "15K"
    elif dsktype.text == "3":
        disktype = "SAS"
    elif dsktype.text == "10":
        disktype = "2000"
    else: 
        disktype = "UNKN"
    return(disktype)

#
#  Telemetry file location
#
if _platform == "win32":
    filedirectory = input("Please enter directory path containing telemetry files:(c:\Telemetryfiles) ")
elif _platform == "linux" or _platform == "linux2" or _platform == "darwin":
    filedirectory = input("Please enter directory path containing telemetry files:(/Telemetryfiles) ")
else:
    sys.exit('OS type not supported')
    
#
#  Parse files in directory
#
if filedirectory == '' and _platform == "win32":
    filedirectory = 'c:\Telemetryfiles\\'
elif filedirectory == '' and (_platform == "linux" or  _platform == "linux2" or _platform == "darwin"):
    filedirectory = '/Telemetryfiles/'

try:
    listing = os.listdir(filedirectory)
except Exception as err:
    print (err)
    wait = input("PRESS ENTER TO CONTINUE.")
    sys.exit(0)

for filename in listing:
    fname, ext = os.path.splitext(filename)
    head = 0
    hosthtml = ''
    sanhtml = ''
    swhtml = ''
    physhtml = ''
    rghtml = ''
#
# Header layout and Stylesheet information
#
    header_string = '''
            <html>
                <head>
                    <style>
                      {
                            padding: 0;
                            margin: 0;
                        } 
                        body {
                            background-color: lightgray;
	                        font: .74em "Trebuchet MS" Verdana, Arial, sans-serif;
	                        line-height: 1.5em; 
                        }
                        h1 {
	                        color: maroon;
	                        text-decoration: underline;
                            margin-left: 40px;
                        }
                        h2 {
	                        color: blue;
	                        text-decoration: italic;
                            margin-left: 40px;
                        }
                        h3 {
	                        color: black;
	                        text-decoration: none;
                            margin-left: 40px;
                        }
                        t1 {
	                        color: black;
	                        text-decoration: none;
                            margin-left: 60px;
                        }
                        #Table1 {
                            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                            width: 80%;
                            border-collapse: collapse;
                            margin-left: 60px;
                        }

                        #Table1  td, #Table1  th {
                            font-size: 1em;
                            border: 2px solid blue;
                            padding: 1px 1px 1px 1px;
                        }

                        #Table1  th {
                            font-size: 1.1em;
                            text-align: left;
                            padding-top: 3px;
                            padding-bottom: 2px;
                            background-color: white;
                            color: black;
                        }

                        #Table1  tr.alt td {
                            color: #000000;
                            background-color: red;
                        }
                        pp {
                            font-size: 1.5em;
                            text-decoration: underline;
                            margin-left: 50px;
                        }
                    </style>
                </head>
                <body>
               '''

    if ext == '.xml':
        f = open(filedirectory + filename + '.txt','w')
        g = open(filedirectory + filename +'.html','w')
        tree = ET.parse(filedirectory + filename)
        root = tree.getroot()
        g.write(header_string)
#
# This code walks the telemetry XML tree using namespaces
#
# Server/Host Information
#
        
        for san in root.findall('SAN:SAN', namespaces):
            #
# SubSystem Information
#
            g.write('''<h1>VNX Configuration and Usage Information</h1>''')
            head = 0
            html_string = ''                     
            for subsystem in san:
                for clariion in subsystem.findall('CLAR:CLARiiON', namespaces):
                    serialno = clariion.find('CLAR:SerialNumber', namespaces)
                    clarname = clariion.find('CLAR:Name', namespaces)
                    clarwwn = clariion.find('CLAR:WWN', namespaces)
                    clarmodel = clariion.find('CLAR:ModelNumber', namespaces)
                    if head == 0:
                       line2 = ("      Array Info    \n")
                       print_header(separater, line2, separater)
                       head = 1
                    line = (" {:<15}".format(clarmodel.text) + "{:<15}".format(clarname.text) + \
                        "{:<15}".format(serialno.text) + "{:<20}".format(clarwwn.text) + "\n")
                    f.write(line)
                    g.write('''<pp>''' + line+ '''</pp>''')     





            for servers in san.findall('SAN:Servers', namespaces):
                html_string = '''
                     <table id="Table1">
                      <tr>
                        <th>Server Name</th>
                        <th>Server Type</th>
                        <th>IP Address</th>
                        <th>SP Connections</th>
                        <th>Device Driver</th>
                      </tr>'''
                g.write(html_string)
                for server in servers.findall('SAN:Server', namespaces):
                    hostname = server.find('SAN:HostName', namespaces)
                    ipa = server.find('SAN:HostIPAddress', namespaces)
                    totports = 0          
                    for hbainfo in server.findall('SAN:HBAInfo', namespaces):
                        numberofports = hbainfo.find('SAN:NumberOfHBAPorts', namespaces)
                        totports = totports + int(numberofports.text)            
                        for hbaports in hbainfo.findall('SAN:HBAPorts', namespaces):
                            for hbaport in hbaports.findall('SAN:HBAPort', namespaces):
                                devicedrivername = hbaport.find('SAN:DeviceDriverName', namespaces)
                                vendordescription = hbaport.find('SAN:VendorDescription', namespaces)
                                if head == 0:
                                   line2 = ("     Host Info     \n")
                                   print_header(separater, line2, separater)
                                   head = 1
                                if devicedrivername is None:
                                   line = (" {:<30}".format(hostname.text) + " {:50}".format(vendordescription.text) + "\n" + \
                                       "            {:<18}".format(ipa.text) + "{:<2}".format(str(totports)) + "\n")
                                   f.write(line)
                                   g.write('''<tr> <td>''' + " {:<30}".format(hostname.text) + '''</td>''' + \
                                        '''<td>''' + " {:50}".format(vendordescription.text) +'''</td>''' + \
                                        '''<td>''' + "{:<18}".format(ipa.text) + '''</td>''' + \
                                        '''<td>''' + "{:<2}".format(str(totports))  + '''</td>''' + \
                                        '''<td>''' + '''UNKNOWN'''  + '''</td></tr>''')                         
                                else:
                                   line = (" {:<30}".format(hostname.text)  +" {:50}".format(vendordescription.text) + "\n" +\
                                       "            {:<18}".format(ipa.text) + \
                                       "{:<2}".format(str(totports)) + devicedrivername.text +"\n")
                                   f.write(line)                           
                                   g.write('''<tr> <td>''' + " {:<30}".format(hostname.text) + '''</td>''' + \
                                        '''<td>''' + " {:50}".format(vendordescription.text) +'''</td>''' + \
                                        '''<td>''' + "{:<18}".format(ipa.text) + '''</td>''' + \
                                        '''<td>''' + "{:<2}".format(str(totports))  + '''</td>''' + \
                                        '''<td>''' + devicedrivername.text  + '''</td></tr>''') 
                                      
                g.write('''</table>''')      

#
# Software Information
#
                head = 0
                for softwares in clariion.findall('CLAR:Softwares', namespaces):
                    html_string = '''
                     <table id="Table1">
                      <tr>
                        <th>Software Name</th>
                        <th>Revision</th>
                        <th>Description</th>
                        <th>Active?</th>
                      </tr>'''
                    g.write(html_string)
                    for software in softwares.findall('CLAR:Software', namespaces):
                        softname = software.find('CLAR:Name', namespaces)
                        softrev = software.find('CLAR:Revision', namespaces)
                        softdescr = software.find('CLAR:Description', namespaces)
                        softisactive = software.find('CLAR:IsActive', namespaces)
                        active = "Not Active"
                        if softisactive.text == "true":
                           active = "Active"
                        if head == 0:
                            line2 = ("     Software Info  \n")
                            print_header(separater, line2, separater)
                            head = 1
                        line = (" " + "{:<25}".format(softname.text) +\
                                "         {:<55}".format(softdescr.text) + "\n" + "             {:<20}".format(softrev.text) + \
                                "{:<10}".format(active)  +"\n-\n" )
                        f.write(line)
                        g.write('''<tr> <td>''' + " {:<25}".format(softname.text) + '''</td>''' + \
                                    '''<td>''' + " {:20}".format(softrev.text) +'''</td>''' + \
                                    '''<td>''' + "{:<55}".format(softdescr.text) + '''</td>''' + \
                                    '''<td>''' + "{:<10}".format(active)  + '''</td></tr>''')   
                          
                

#
# Physical Information ie. Disks
#
                head = 0
                totalcapacity = 0
                
                for physicals in clariion.findall('CLAR:Physicals', namespaces):
                    for storagesps in physicals.findall('CLAR:StorageProcessors', namespaces):
                        for storagesp in storagesps.findall('CLAR:StorageProcessor', namespaces):
                            spname = storagesp.find('CLAR:Name', namespaces)
                        for disks in physicals.findall('CLAR:Disks', namespaces):
                            html_string = '''
                             <table id="Table1">
                              <tr>
                                <th>Bus Number</th>
                                <th>Enclosure</th>
                                <th>Slot</th>
                                <th>Type</th>
                                <th>Capacity</th>
                              </tr>'''
                            g.write(html_string)
                            for disk in disks.findall('CLAR:Disk', namespaces):
                                busnum = disk.find('CLAR:Bus', namespaces)
                                encnum = disk.find('CLAR:Enclosure', namespaces)
                                slotnum = disk.find('CLAR:Slot', namespaces)
                                dskstate = disk.find('CLAR:State', namespaces)
                                dsktype = disk.find('CLAR:Type', namespaces)
                                dskproduct = disk.find('CLAR:Product', namespaces)
                                capacity = disk.find('CLAR:CapacityInMBs', namespaces)
                                capgb = int(capacity.text) / 1024
                                totalcapacity = totalcapacity + capgb
                                disktype = convert_disk(dsktype)
                                if head == 0:
                                   line2 = ("      Disk Info     \n")
                                   print_header(separater, line2, separater)
                                   head = 1
                                if dskproduct is None:
                                   dskshortname = "EMPTY SLOT "
                                else:
                                   dskshortname = dskproduct.text[-8:]
                                line = ("  Bus Number: " + "{:<5}".format(busnum.text) + " Enclosure: " + \
                                       "{:<5}".format(encnum.text) + "Slot: " + "{:<5}".format(slotnum.text) + \
                                       " Disk Type: " +  "{:<15}".format(dskshortname) + " Capacity(GB) = " + \
                                       str("{0:.2f}".format(capgb)) + "\n")
                                f.write(line)
                                g.write('''<tr> <td>''' + " {:<5}".format(busnum.text) + '''</td>''' + \
                                    '''<td>''' + " {:5}".format(encnum.text) +'''</td>''' + \
                                    '''<td>''' + "{:<5}".format(slotnum.text) + '''</td>''' + \
                                    '''<td>''' + "{:<15}".format(dskshortname)  + '''</td>''' + \
                                    '''<td>''' + str("{0:.2f}".format(capgb)) + '''</tr>''')
# Write total capacity to file and html table
                f.write("Total Capacity in TB = " + str("{0:.2f}".format(totalcapacity/1024)) + "\n")
                g.write('''<tr> <td>''' + " " + '''</td>''' + \
                    '''<td>''' + " " +'''</td>''' + \
                    '''<td>''' + " " + '''</td>''' + \
                    '''<td>''' + "Total Capacity"  + '''</td>''' + \
                    '''<td>''' + str("{0:.2f}".format(totalcapacity)) + '''</tr>''')
#
# RaidGroup Information
#
                head = 0
                
                for logicals in clariion.findall('CLAR:Logicals', namespaces):
                    for raidgroups in logicals.findall('CLAR:RAIDGroups', namespaces):
                        header_string = '''
                             <table id="Table1">
                              <tr>
                                <th>Raid Grp ID</th>
                                <th>Raid Grp Capacity</th>
                                <th>Raid Grp Free</th>
                              </tr>'''

                        if head == 0:
                           line2 = ("     Raid Group Info     \n")
                           print_header(separater, line2, separater)
                           head = 1
                        for raidgroup in raidgroups.findall('CLAR:RAIDGroup', namespaces):
                            raidgrpid = raidgroup.find('CLAR:ID', namespaces)
                            raidgrpfree = int(raidgroup.find('CLAR:FreeSpace', namespaces).text) /2048 /1024
                            raidgrpcap = raidgroup.find('CLAR:Capacity', namespaces)
                            raidcapacity = int(raidgrpcap.text) / 2048 / 1024
                            raidgrptype = raidgroup.find('CLAR:RGRaidType', namespaces)
                            raidgrpispvt = raidgroup.find('CLAR:IsPrivate', namespaces)
                            raidgrprawcap = raidgroup.find('CLAR:RawCapacityBlocks', namespaces)
                            line = ("  Raid Group ID: " + "{:<5}".format(raidgrpid.text) + "  Raid Group Cap (GB): " +  str("{0:.2f}".format(raidcapacity)) + \
                                " Raid Group Free (GB): " + str("{0:.2f}".format(raidgrpfree)) +"\n")
                            f.write(line)
                            g.write(header_string)
                            g.write('''<tr> <td>''' + " {:<5}".format(raidgrpid.text) + '''</td>''' + \
                                '''<td>''' + str("{0:.2f}".format(raidcapacity))  + '''</td>''' + \
                                '''<td>''' + str("{0:.2f}".format(raidgrpfree)) + '''</tr>''')
#
                            head = 0
                            if head == 0:
                               line2 = ("     Raid Group Disks     \n")
                               print_header(separater, line2, separater)
                               head = 1
                               rghtml = rghtml + line2 
                            for rdsks in raidgroup.findall('CLAR:Disks', namespaces):
                                html_string = '''
                                     <table id="Table1">
                                      <tr>
                                        <th>Raid Grp Disks</th>
                                      </tr>
                                       <tr>
                                        <th>Bus</th>
                                        <th>Enclosure</th>
                                        <th>Slot</th>
                                      </tr>'''
                                g.write(html_string)
                                for rdsk in rdsks.findall('CLAR:Disk', namespaces):
                                    bus = rdsk.find('CLAR:Bus', namespaces)
                                    enclosure = rdsk.find('CLAR:Enclosure', namespaces)
                                    slot = rdsk.find('CLAR:Slot', namespaces)
                                    line = ("      Bus: " + "{:<5}".format(bus.text) + "Enclosure: " + "{:<5}".format(enclosure.text) + "Slot: " + "{:<5}".format(slot.text) + "\n")
                                    g.write('''<tr> <td>''' + " {:<5}".format(bus.text) + '''</td>''' + \
                                        '''<td>''' + "{:<5}".format(enclosure.text)  + '''</td>''' + \
                                        '''<td>''' + "{:<5}".format(slot.text) + '''</tr>''')
                                    f.write(line)
                                f.write("\n" + separater)
#
#  Write the end of the HTML file
#
                html_string = '''
                    </body>
                </html>'''
                g.write(html_string)
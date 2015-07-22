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
listing = os.listdir(filedirectory)    
for filename in listing:
    fname, ext = os.path.splitext(filename)
    head = 0
    if ext == '.xml':
        f = open(filedirectory + filename + '.txt','w')
        tree = ET.parse(filedirectory + filename)
        root = tree.getroot()
#
# This code walks the telemetry XML tree using namespaces
#
        for san in root.findall('SAN:SAN', namespaces):
            for servers in san.find('SAN:Servers', namespaces):
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
                                else:
                                   line = (" {:<30}".format(hostname.text)  +" {:50}".format(vendordescription.text) + "\n" +\
                                       "            {:<18}".format(ipa.text) + \
                                       "{:<2}".format(str(totports)) + devicedrivername.text +"\n")
                                   f.write(line)

                    
        #
        # Host Level Information
        #
        head = 0                     
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

        #
        # Software Information
        #
                head = 0
                for softwares in clariion.findall('CLAR:Softwares', namespaces):
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

                head = 0
                totalcapacity = 0

        #
        # Physical Information ie. Disks
        #
                for physicals in clariion.findall('CLAR:Physicals', namespaces):
                    for storagesps in physicals.findall('CLAR:StorageProcessors', namespaces):
                        for storagesp in storagesps.findall('CLAR:StorageProcessor', namespaces):
                            spname = storagesp.find('CLAR:Name', namespaces)
                        for disks in physicals.findall('CLAR:Disks', namespaces):
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
                                   line = ("  Bus Number: " + "{:<5}".format(busnum.text) + " Enclosure: " + \
                                       "{:<5}".format(encnum.text) + "Slot: " + "{:<5}".format(slotnum.text) + \
                                       " Disk Type: EMPTY SLOT " + "\n")
                                else:
                                   dskshortname = dskproduct.text[-8:]
                                   line = ("  Bus Number: " + "{:<5}".format(busnum.text) + " Enclosure: " + \
                                       "{:<5}".format(encnum.text) + "Slot: " + "{:<5}".format(slotnum.text) + \
                                       " Disk Type: " +  "{:<15}".format(dskshortname) + " Capacity(GB) = " + \
                                       str("{0:.2f}".format(capgb)) + "\n")
                                f.write(line)
                f.write("Total Capacity in TB = " + str("{0:.2f}".format(totalcapacity/1024)) + "\n")
        #
        # RaidGroup Information
        #
                head = 0
                for logicals in clariion.findall('CLAR:Logicals', namespaces):
                    for raidgroups in logicals.findall('CLAR:RAIDGroups', namespaces):
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
                            head = 0
                            if head == 0:
                               line2 = ("     Raid Group Disks     \n")
                               print_header(separater, line2, separater)
                               head = 1
                            for rdsks in raidgroup.findall('CLAR:Disks', namespaces):
                                for rdsk in rdsks.findall('CLAR:Disk', namespaces):
                                    bus = rdsk.find('CLAR:Bus', namespaces)
                                    enclosure = rdsk.find('CLAR:Enclosure', namespaces)
                                    slot = rdsk.find('CLAR:Slot', namespaces)
                                    line = ("      Bus: " + "{:<5}".format(bus.text) + "Enclosure: " + "{:<5}".format(enclosure.text) + "Slot: " + "{:<5}".format(slot.text) + "\n")
                                    f.write(line)
                                f.write("\n" + separater)







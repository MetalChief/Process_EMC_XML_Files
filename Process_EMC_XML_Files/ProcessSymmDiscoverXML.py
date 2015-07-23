from xml.etree import ElementTree as ET
from sys import platform as _platform
import os 
import sys

if _platform == "win32":
    filedirectory = input("Please enter directory path containing SymmDiscover files:(c:\SymmDiscoverFiles) ")
elif _platform == "linux" or _platform == "linux2" or _platform == "darwin":
    filedirectory = input("Please enter directory path containing SymmDiscover files:(/SymmDiscoverFiles) ")
else:
    sys.exit('OS type not supported')


if filedirectory == '' and _platform == "win32":
    filedirectory = 'c:\SymmDiscoverFiles\\'
elif filedirectory == '' and (_platform == "linux" or  _platform == "linux2" or _platform == "darwin"):
    filedirectory = '/SymmDiscoverFiles/'

try:
    listing = os.listdir(filedirectory)
except Exception as err:
    print (err)
    wait = input("PRESS ENTER TO CONTINUE.")
    sys.exit(0)


for filename in listing:
    fname, ext = os.path.splitext(filename)
    head = 0
    if ext == '.xml':
        f = open(filedirectory + filename + '.txt','w')
        tree = ET.parse(filedirectory + filename)
        root = tree.getroot()
#
# Handles SymmDiscoverPool.xml
#
    if filename == "SymDiscoverPool.xml":
        for symm in root.findall('Symmetrix'):
            for pool in symm.findall('DevicePool'):
                poolname = pool.find('pool_name')
                raidcfg = pool.find('dev_config')
                total_usable_tb = pool.find('total_usable_tracks_tb')
                total_used_tb = pool.find('total_used_tracks_tb')
                total_free_tb = pool.find('total_free_tracks_tb')
                percent_full = pool.find('percent_full')
                line = ("Pool Name: " + poolname.text + \
                    "\n          Raid Cfg: " + raidcfg.text + \
                    "\n          Total TB: " + total_usable_tb.text + \
                    "\n           Used TB: " + total_used_tb.text + \
                    "\n           Free TB: " + total_free_tb.text + \
                    "\n      Percent Full: " + percent_full.text + \
                    "\n-------------------------------------------------\n")
                f.write(line)
#
# Handles SymmDiscoverPolicy.xml
#
    if filename == "SymDiscoverPolicy.xml":
        for symm in root.findall('Symmetrix'):
            for symminfo in symm.findall('Symm_Info'):
                symid = symminfo.find('symid')
                f.write("Symmetrix SN: " + symid.text + "\n")
            for fastpolicy in symm.findall('Fast_Policy'):
                for policyinfo in fastpolicy.findall('Policy_Info'):
                    policyname = policyinfo.find('policy_name')
                    numberoftiers = policyinfo.find('num_of_tiers')
                    line = ("Policy Name: " + policyname.text + \
                        "\n   Number of Tiers: " + numberoftiers.text + \
                        "\n")
                for tier in fastpolicy.findall('Tier'):
                    tiername = tier.find('tier_name')
                    tiertype = tier.find('tier_type')
                    tiermaxsgper = tier.find('tier_max_sg_per')
                    tierprotection = tier.find('tier_protection')
                    tiertech = tier.find('tier_tech')
                    line = ("     Tier Name: " + tiername.text + \
                        "\n              Tier Type: " + tiertype.text + \
                        "\n                Max SGs: " + tiermaxsgper.text + \
                        "\n              Tier Prot: " + tierprotection.text + \
                        "\n              Tier Tech: " + tiertech.text + \
                        "\n-------------------------------------------------\n")
                    f.write(line)
#
# Handles SymmDiscoverTier.xml
#
    if filename == "SymDiscoverTier.xml":
        for symm in root.findall('Symmetrix'):
            for symminfo in symm.findall('Symm_Info'):
                symid = symminfo.find('symid')
                f.write("Symmetrix SN: " + symid.text + "\n")
            for stgtier in symm.findall('Storage_Tier'):
                for tierinfo in stgtier.findall('Tier_Info'):
                    tiername = tierinfo.find('tier_name')
                    tiertype = tierinfo.find('tier_type')
                    tiertech = tierinfo.find('technology')
                    tierprot = tierinfo.find('target_protection')
                    numofpools= tierinfo.find('num_of_pools')
                    line = ("Tier Name: " + tiername.text + \
                       "\n         Tier Tech: " + tiertech.text + \
                       "\n         Tier Type: " + tiertype.text + \
                       "\n         Tier Prot: " + tierprot.text + \
                       "\n      Num of Pools: " + numofpools.text + \
                       "\n-------------------------------------------------\n")
                    f.write(line)
                    for thinpoolinfo in tierinfo.findall('Thin_Pool_Info'):
                        poolname = thinpoolinfo.find('pool_name')
                        poolengb = thinpoolinfo.find('enabled_gb')
                        poolfrgb = thinpoolinfo.find('free_gb')
                        poolusgb = thinpoolinfo.find('used_gb')
                        poolprcf = thinpoolinfo.find('full_percent')                       
                        line = ("Pool Name: " + poolname.text + \
                            "\n        Enabled GB: " + poolengb.text + \
                            "\n           Free GB: " + poolfrgb.text + \
                            "\n           Used GB: " + poolusgb.text + \
                            "\n      Percent Full: " + poolprcf.text + \
                            "\n-------------------------------------------------\n")
                        f.write(line)
                             

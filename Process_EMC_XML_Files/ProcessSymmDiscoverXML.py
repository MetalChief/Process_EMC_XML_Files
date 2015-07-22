from xml.etree import ElementTree as ET

tree = ET.parse('SymDiscoverPool.xml')
root = tree.getroot()
for symm in root.findall('Symmetrix'):
    for pool in symm.findall('DevicePool'):
        poolname = pool.find('pool_name')
        print(poolname.text)
        raidcfg = pool.find('dev_config')
        print(raidcfg.text)
#        total_tb = pool.find('total_tracks_tb')
#        print(total_tb.text)
        total_usable_tb = pool.find('total_usable_tracks_tb')
        print(total_usable_tb.text)
        total_used_tb = pool.find('total_used_tracks_tb')
        print(total_used_tb.text)
        total_free_tb = pool.find('total_free_tracks_tb')
        print(total_free_tb.text)
        percent_full = pool.find('percent_full')
        print(percent_full.text)
    
                             

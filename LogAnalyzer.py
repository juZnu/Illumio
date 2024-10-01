from file_location import LOG_FILE, LOOKUP_FILE, PROTOCOL_FILE, TAG_COUT_OUTPUT, PORT_PROTOCOL_OUTPUT
from variables import LOG_KEYS, SKIP

def createProtocolList(protocol_file):

    protocolList = ['Unassigned'] * 256
    with open(protocol_file, mode='r') as file:

        next(file)
        for line in file:
            try:
                parts = line.strip().split(',')
                decimal = int(parts[0].strip()) 
                protocol = parts[1].strip().lower() 
                
                if not protocol: 
                    continue
                
                protocolList[decimal] = protocol
            except ValueError:
                continue

    return protocolList

def createLookupMap(lookup_file):
    Map = dict()
    

    with open(lookup_file, mode='r') as file:

        next(file)
        for line in file:

            parts = line.strip().split(',')
            if len(parts) < 3:
                continue 
            
            port = parts[0].strip()
            protocol = parts[1].strip().lower()
            tag = parts[2].strip()

            key = f'{port}_{protocol}'
            Map[key] = tag
            
    return Map


def createLogMap(log_str):
    Map = dict()
    
    for key,value in zip(LOG_KEYS,log_str.split(' ')):
        Map[key] = value
        
    return Map

def createOutputFile(filepath,output,header = ''):

    with open(filepath, mode='w') as file:
        file.write(header)

        for key,value in output.items():
            row = f'{key},{value}'
            file.write(row + '\n')
    

def analyzeLogs(log_file,protocol_file ,lookup_file ,tag_output_file,port_protocol_file,skip = ''):
    protocols = createProtocolList(protocol_file)
    lookupMap = createLookupMap(lookup_file)
    
    tagMap = dict()
    portProtocolMap = dict()
    
    with open(log_file, mode='r') as file:
        for line in file:
            line = line.strip()
            
            if not line: continue
            
            logMap = createLogMap(line)
            
            if logMap['action'] == skip or logMap['version'] != 2:
                continue
            
            port = logMap['dstport']
            protocol = int(logMap['protocol'])
            
            lookupkey = f'{port}_{protocols[protocol]}'
            key = lookupMap.get(lookupkey, 'Untagged')
            tagMap[key] = tagMap.get(key,0) + 1
            
            portProtocolKey = f"{port},{protocols[protocol]}"
            portProtocolMap[portProtocolKey] = portProtocolMap.get(portProtocolKey, 0) + 1
        
        createOutputFile(tag_output_file,tagMap,'Tag,Count\n')
        createOutputFile(port_protocol_file,portProtocolMap,'Port,Protocol,Count\n')
    

def main():
    analyzeLogs(LOG_FILE,PROTOCOL_FILE,LOOKUP_FILE,TAG_COUT_OUTPUT,PORT_PROTOCOL_OUTPUT,SKIP)

if __name__ == "__main__":
    main()
    



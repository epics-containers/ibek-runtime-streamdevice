Commands = {
            '\x00' : {
                     "Name":"Get status",
                     "RequestLength":'\x02',
                     "ReplyLength":'\x12',
                     "Command":'\x00',
                     "RequestDataBytes":0,
                     "ReplyDataBytes":16
                     },
            '\x01' : {
                     "Name":"Acknowledge errors",
                     "RequestLength":'\x0A',
                     "ReplyLength":'\x02',
                     "Command":'\x01',
                     "RequestDataBytes":8,
                     "ReplyDataBytes":0
                     },
            '\x02' : {
                     "Name":"Start",
                     "RequestLength":'\x02',
                     "ReplyLength":'\x02',
                     "Command":'\x02',
                     "RequestDataBytes":0,
                     "ReplyDataBytes":0
                     },
            '\x03' : {
                     "Name":"Stop",
                     "RequestLength":'\x02',
                     "ReplyLength":'\x02',
                     "Command":'\x03',
                     "RequestDataBytes":0,
                     "ReplyDataBytes":0
                     },
            '\x04' : {
                     "Name":"ReadValue",
                     "RequestLength":'\x03',
                     "ReplyLength":'\x07',
                     "Command":'\x04',
                     "RequestDataBytes":1,
                     "ReplyDataBytes":5
                     },
            '\x05' : {
                     "Name":"WriteValue",
                     "RequestLength":'\x08',
                     "ReplyLength":'\x02',
                     "Command":'\x05',
                     "RequestDataBytes":6,
                     "ReplyDataBytes":0
                     }
            }
VariableTypes = {
                'Int16': {
                         'ByteCode':'\x01',
                         'pFormat':'i' # python format 
                         },#not using h because value should be transmitted as 4 bytes
                'Uint16': {
                         'ByteCode':'\x02',
                         'pFormat':'I'
                         },#not using H because value should be transmitted as 4 bytes
                'Int32': {
                         'ByteCode':'\x03',
                         'pFormat':'i'
                         },
                'Uint32': {
                         'ByteCode':'\x04',
                         'pFormat':'I'
                         },
                'Float': {
                         'ByteCode':'\x05',
                         'pFormat':'f'
                         }
                }
Variables = {
                '\x00' : {
                         "Name":"Reference speed",
                         "Type":"Int32",
                         "SimValue":467, #rpm
                         "Fluctuating":1
                         },
                '\x01' : {
                         "Name":"Actual Speed",
                         "Type":"Int32",
                         "SimValue":1300, # rpm
                         "Fluctuating":1                         
                         },
                '\x02' : {
                         "Name":"Measured DC-Link current",
                         "Type":"Int16",
                         "SimValue":666, # mA
                         "Fluctuating":1                         
                         },
                '\x03' : {
                         "Name":"Current reference",
                         "Type":"Int16",
                         "SimValue":945, # mA
                         "Fluctuating":1                         
                         },
                '\x04' : {
                         "Name":"Converter temperature",
                         "Type":"Int16",
                         "SimValue":26, # celcius degrees
                         "Fluctuating":1                         
                         },
                '\x05' : {
                         "Name":"DC-Link voltage",
                         "Type":"Int16",
                         "SimValue":12, # V
                         "Fluctuating":1                         
                         },
                '\x06' : {
                         "Name":"Output power",
                         "Type":"Int16",
                         "SimValue":45, # W
                         "Fluctuating":1                         
                         },
                '\x07' : {
                         "Name":"Motor temperature (THC)",
                         "Type":"Int16",
                         "SimValue":42, # celcius degrees
                         "Fluctuating":1                         
                         },
                '\x08' : {
                         "Name":"Motor temperature (PTC)",
                         "Type":"Int16",
                         "SimValue":31, # celcius degrees
                         "Fluctuating":1                         
                         },
                '\x09' : {
                         "Name":"Pole pairs",
                         "Type":"Uint16",
                         "SimValue":0, #
                         "Fluctuating":0                         
                         },
                '\x0A' : {
                         "Name":"Max phase current",
                         "Type":"Int16",
                         "SimValue":320, # mA
                         "Fluctuating":1                         
                         },
                '\x0B' : {
                         "Name":"Max rotational speed",
                         "Type":"Int32",
                         "SimValue": 222, # 
                         "Fluctuating":0                         
                         },
                '\x0C' : {
                         "Name":"Synchronization current",
                         "Type":"Uint16",
                         "SimValue": 234, # 
                         "Fluctuating":1                         
                         },
                '\x0D' : {
                         "Name":"Axial moment of inertia",
                         "Type":"Float",
                         "SimValue": 3.5, # 
                         "Fluctuating":1                         
                         },
                '\x0E' : {
                         "Name":"PM Flux linkage",
                         "Type":"Float",
                         "SimValue": 11.3, # 
                         "Fluctuating":1                         
                         },
                '\x0F' : {
                         "Name":"Phase inductance",
                         "Type":"Float",
                         "SimValue": 8.3, # 
                         "Fluctuating":1                         
                         },                         
                '\x10' : {
                         "Name":"Phase resistance",
                         "Type":"Float",
                         "SimValue": 42.3, # 
                         "Fluctuating":1                         
                         },
                '\x11' : {
                         "Name":"Rotation direction",
                         "Type":"Uint16",
                         "SimValue": 0, # 
                         "Fluctuating":0                         
                         },
                '\x12' : {
                         "Name":"Acc. ratio (above sync.)",
                         "Type":"Float",
                         "SimValue": 5.12, # 
                         "Fluctuating":0
                         },
                '\x13' : {
                         "Name":"Acc. ratio (below sync.)",
                         "Type":"Float",
                         "SimValue": 2.5, # 
                         "Fluctuating":0                         
                         },
                '\x14' : {
                         "Name":"Speed controller raise time",
                         "Type":"Float",
                         "SimValue": 5.6, # 
                         "Fluctuating":0                         
                         },
                '\x15' : {
                         "Name":"User defined sync. Speed",
                         "Type":"Uint16",
                         "SimValue": 600, # 
                         "Fluctuating":0
                         },
                '\x16' : {
                         "Name":"Default sync speed (lower)",
                         "Type":"Int32",
                         "SimValue": 125, # rpm
                         "Fluctuating":0                         
                         },
                '\x17' : {
                         "Name":"Default sync speed (upper)",
                         "Type":"Int32",
                         "SimValue": 700,  # rpm
                         "Fluctuating":0                         
                         },
                '\x18' : {
                         "Name":"User def. sync speed (lower)",
                         "Type":"Int32",
                         "SimValue": 400,  #
                         "Fluctuating":0
                         },
                '\x19' : {
                         "Name":"User def. sync speed (upper)",
                         "Type":"Int32",
                         "SimValue": 900, # 
                         "Fluctuating":0                         
                         },
                '\x1A' : {
                         "Name":"User defined control parameter",
                         "Type":"Uint16",
                         "SimValue": 0, # 
                         "Fluctuating":0
                         },
                '\x1B' : {
                         "Name":"Proportional speed gain",
                         "Type":"Float",
                         "SimValue": 0.4, # 
                         "Fluctuating":0
                         },
                '\x1C' : {
                         "Name":"Integral speed gain",
                         "Type":"Float",
                         "SimValue": 0.3, # 
                         "Fluctuating":0                         
                         },
                '\x1D' : {
                         "Name":"Levitate",
                         "Type":"Uint16",
                         "SimValue": 0, # 
                         "Fluctuating":0                         
                         }                
                }
ErrorCodes = {
    "UNKNOWN_COMMAND" : {
        "ByteSequence"  : '\x01\x40\x00\x00',
        "Simulate"      : 1
    },
    "WRONG_CHECKSUM" : {
        "ByteSequence"  : '\x02\x40\x00\x00',
        "Simulate"      : 0
    },
    "INVALID_FORMAT" : {
        "ByteSequence"  : '\x04\x40\x00\x00',
        "Simulate"      : 0
    },
    "READONLY" : {
        "ByteSequence"  : '\x08\x40\x00\x00',
        "Simulate"      : 0
    },
    "TYPEMISMATCH" : {
        "ByteSequence"  : '\x10\x40\x00\x00',
        "Simulate"      : 0
    },
    "UNKNOWN_VARIABLE" : {
        "ByteSequence"  : '\x20\x40\x00\x00',
        "Simulate"      : 1
    }                
}
OKCode                          = '\x00\x00\x00\x00'
WarningCode                     = '\x00\x00\x00\x00' # not used
InfoCode                        = '\x00\x00\x00\x00' # not used
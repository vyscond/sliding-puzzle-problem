import pyopencl as openCL

#  _____ _____ _   _ ______ _____ _____  ______ _       ___  _____  _____ 
# /  __ \  _  | \ | ||  ___|_   _|  __ \ |  ___| |     / _ \|  __ \/  ___|
# | /  \/ | | |  \| || |_    | | | |  \/ | |_  | |    / /_\ \ |  \/\ `--. 
# | |   | | | | . ` ||  _|   | | | | __  |  _| | |    |  _  | | __  `--. \
# | \__/\ \_/ / |\  || |    _| |_| |_\ \ | |   | |____| | | | |_\ \/\__/ /
#  \____/\___/\_| \_/\_|    \___/ \____/ \_|   \_____/\_| |_/\____/\____/ 
#                                                                        

class Platform :

    INTEL       = 'Intel(R) OpenCL'
    NVIDIA_CUDA = 'NVIDIA CUDA'

class DeviceType :    

    #ACCELERATOR = [ 0 , 'ACCELERATOR' ]
    #ALL         = [ 1 , 'ALL'         ]
    CPU          = [ 2 , 'CPU'         ]
    #DEFAULT     = [ 3 , 'DEFAULT'     ]
    GPU          = [ 4 , 'GPU'         ]

class Execution :

    SYNC  = 0
    ASYNC = 1

# ______                 __                           _           _  ______ _       _    __                       _____                           _             
# | ___ \               / _|                         | |         | | | ___ \ |     | |  / _|                     |  __ \                         | |            
# | |_/ / __ ___ ______| |_ ___  _ __ _ __ ___   __ _| |_ ___  __| | | |_/ / | __ _| |_| |_ ___  _ __ _ __ ___   | |  \/ ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
# |  __/ '__/ _ \______|  _/ _ \| '__| '_ ` _ \ / _` | __/ _ \/ _` | |  __/| |/ _` | __|  _/ _ \| '__| '_ ` _ \  | | __ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
# | |  | | |  __/      | || (_) | |  | | | | | | (_| | ||  __/ (_| | | |   | | (_| | |_| || (_) | |  | | | | | | | |_\ \  __/ | | |  __/ | | (_| | || (_) | |   
# \_|  |_|  \___|      |_| \___/|_|  |_| |_| |_|\__,_|\__\___|\__,_| \_|   |_|\__,_|\__|_| \___/|_|  |_| |_| |_|  \____/\___|_| |_|\___|_|  \__,_|\__\___/|_|   
#                                                                                                                                                              

def get_intel_context( ): # intel platform

    return build_especific_context( Platform.INTEL , DeviceType.CPU )

def get_nvidia_cuda_context( ):

    return build_especific_context( Platform.NVIDIA_CUDA , DeviceType.GPU )

def build_especific_context( platform_name , device_type ):

    platform = None

    devices  = []

    # -----------------------------------------------
    # Platform

    for available_platform in openCL.get_platforms() :

        if available_platform.name == platform_name :

            platform = available_platform

            break

    if not platform :

        print 'failed at validating platform'

        exit( 0 )

    # -----------------------------------------------
    # Device
    
    for available_device in platform.get_devices( ):
        
        if available_device.type in device_type :
            
            print '[found device] ' , available_device.name

            devices.append( available_device )
        
    # -----------------------------------------------
    # Context (red orb)

    if len( devices ) > 0 :

        return openCL.Context( devices = devices , dev_type = None )


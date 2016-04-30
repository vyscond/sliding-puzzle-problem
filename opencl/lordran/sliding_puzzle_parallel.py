
import pyopencl as openCL
import numpy
import time

# -------------------------------------------------------------------
# Only exist to help us on fitness preprocessors :D
# -------------------------------------------------------------------
class Puzzle :
    
    def __init__( self , instance ):
        
        if ( len( instance ) / pow( len( instance ) , 0.5 ) ):
            
            print 'valid puzzle'
        
        else :
            
            print 'not a valid puzzle'
            
            exit( 0 )
        
        # -------------------------------
        
        self.instance          = instance
        
        self.size              = len( instance )
        
        self.side_factor       = int( pow( self.size , 0.5 ) )
        
        self.bottom_left_index = self.side_factor * ( self.side_factor - 1 )
        
        self.move_bot          = -(self.side_factor)
        
        self.move_top          = self.side_factor

class RandomNumberList :

    def __init__( self ,  context ):

        self.context = context
        
        try :
            
            #~ self.kernel  = ''.join( open( 'lordran/kernels/CPU_random_number_list.cl' ) )
            self.kernel  = ''.join( open( 'lordran/kernels/CPU_RP_random_number_list.cl' ) )

        except :

            print '[error] some kernel are not available'

            exit(0)

    def execute( self , execution_mode , list_length , raffle_range ):

        #~ cl_raffle_range  = numpy.int32 ( raffle_range ) # limite do sorteio " de 0 ate raffle_range "
        
        cl_drawn_numbers = numpy.array ( range( list_length ) , dtype=numpy.int32 )

        # --- devices ---

        #~ cl_raffle_range_device  = openCL.Buffer( self.context , openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR , hostbuf = cl_raffle_range )

        cl_drawn_numbers_device = openCL.Buffer( self.context , openCL.mem_flags.WRITE_ONLY , cl_drawn_numbers.nbytes )
        
        # --- replace tag on kernel
        
        self.kernel = self.kernel.replace( '[REPLACE_UPPER_LIMIT]' , str(raffle_range) )
        self.kernel = self.kernel.replace( '[REPLACE_LOWER_LIMIT]' , str(0)            )
        
        # --- loading kernel
        
        program = openCL.Program( self.context , self.kernel ).build()
        
        queue   = openCL.CommandQueue( self.context , properties = execution_mode )
        
        event   = program.random_number_list( queue , cl_drawn_numbers.shape , cl_drawn_numbers_device )

        event.wait()

        openCL.enqueue_copy( queue , cl_drawn_numbers , cl_drawn_numbers_device )
        
        cl_drawn_numbers_device.release()

        return cl_drawn_numbers

class InitialPopulationGeneratorEnhanced :

    def __init__( self , context , debug = False):

        self.context = context
        
        try :
            
            if debug :
                
                self.kernel = ''.join( open( 'lordran/kernels/CPU_DEBUG_RP_initial_population.cl' ) )

            else :

                self.kernel = ''.join( open( 'lordran/kernels/CPU_RP_initial_population.cl' ) )

            #print '[python][population generator] kernel was loaded'
            
        except :
            
            print '[python][error] some kernel are no available'
            
            exit(0)
            
    def execute( self , execution_mode ,  chromossome_sizes_list , nucleic_acid_list ): # chromossome_lentghs_list is the offset list
        
        # --- so we cant create a matrix where the columns have different size!
        # --- the solution is work with a offset. So we need to pick/recognize 
        # --- the maximum value of a column and create the matrix based on this
        # --- (because we have a array with the size of each chromossome its possibles to solve this by max() function)
        # --- and then we can "flag" the offset limit on the kernel_loop
        
        MAX_CHROMOSSOME_SIZE = max(chromossome_sizes_list)
        
        # --- generated chromossomes will be stored here
        cl_initialized_chromossome_population  = numpy.zeros( ( len(chromossome_sizes_list) , MAX_CHROMOSSOME_SIZE ) , dtype = numpy.int32 )
        
        # --- values for chromossomes
        cl_nucleic_acid_values_list = numpy.array( nucleic_acid_list , dtype = numpy.int32 )
        
        # --- list with the sizes from each chromossome
        cl_offset_list = numpy.array( chromossome_sizes_list , dtype = numpy.int32 )
        
        
        # --- devices ---
        
        cl_initialized_chromossome_population_device  = openCL.Buffer( self.context , openCL.mem_flags.WRITE_ONLY | openCL.mem_flags.COPY_HOST_PTR , size = cl_initialized_chromossome_population.nbytes , hostbuf = cl_initialized_chromossome_population)
        
        cl_nucleic_acid_list_device = openCL.Buffer( self.context , openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR , hostbuf = cl_nucleic_acid_values_list      ) 
        
        cl_offset_list_device       = openCL.Buffer( self.context , openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR , hostbuf = cl_offset_list     ) 
        
        # --- replacing tag at KERNEL
         
        self.kernel = self.kernel.replace( '[REPLACE_CHROMOSSOME_MAXIMUM_SIZE]' , str( MAX_CHROMOSSOME_SIZE ) )
        self.kernel = self.kernel.replace( '[REPLACE_NUCLEIC_ACID_LIST_LEN]'    , str( len( nucleic_acid_list     ) ) )
        
        # --- loading kernel
        
        program = openCL.Program( self.context , self.kernel ).build()
        
        queue = openCL.CommandQueue( self.context , properties = execution_mode )

        event = program.generate_initial_population(

                    queue , 
                    
                    cl_initialized_chromossome_population.shape ,
                    
                    cl_initialized_chromossome_population_device ,
                    
                    cl_offset_list_device , 
                    
                    cl_nucleic_acid_list_device 
                )
        
        event.wait()
        
        openCL.enqueue_copy( queue , cl_initialized_chromossome_population , cl_initialized_chromossome_population_device )
        
        cl_initialized_chromossome_population_device.release()
        cl_nucleic_acid_list_device.release()
        cl_offset_list_device.release()
        
        # --- cleaning zeros ---
        
        #return self.remove_zeros( cl_initialized_chromossome_population )
        
        return  ( list(cl_initialized_chromossome_population) , list(chromossome_sizes_list) , MAX_CHROMOSSOME_SIZE ) 

class InitialPopulationGenerator : 

    # ---------------------------------------------------
    #      _                               _           _ 
    #     | |                             | |         | |
    #   __| | ___ _ __  _ __ ___  ___ __ _| |_ ___  __| |
    #  / _` |/ _ \ '_ \| '__/ _ \/ __/ _` | __/ _ \/ _` |
    # | (_| |  __/ |_) | | |  __/ (_| (_| | ||  __/ (_| |
    #  \__,_|\___| .__/|_|  \___|\___\__,_|\__\___|\__,_|
    #           | |                                     
    #           |_|                                     
    # ---------------------------------------------------

    def __init__( self , context ):

        self.context = context
        
        try :
        
            self.debug_kernel = ''.join( open('lordran/kernels/CPU_DEBUG_initial_population.cl') ) 
            self.kernel       = ''.join( open( 'lordran/kernels/CPU_initial_population.cl' ) )
            
            print 'kernel was loaded'

        except :

            print '[error] some kernel are no available'

            exit(0)
        
    def execute( self , execution_mode ,  chromossome_size_list , nucleic_acid_list ): # chromossome_lentghs_list is the offset list
        
        # --- so we cant create a matrix where the columns have different size!
        # --- the solution is work with a offset. So we need to pick/recognize 
        # --- the maximum value of a column and create the matrix based on this
        # --- (because we have a array with the size of each chromossome its possibles to solve this by max() function)
        # --- and then we can "flag" the offset limit on the kernel_loop
        
        # --- generated chromossomes
        cl_initialized_chromossome_population  = numpy.zeros( ( len(chromossome_size_list) , max(chromossome_size_list) ) , dtype = numpy.int32 )
        
        # --- values for chromossomes
        cl_nucleic_acid_values_list            = numpy.array( nucleic_acid_list                                           , dtype = numpy.int32 )
        
        # --- size of this values
        cl_nucleic_acid_values_list_size       = numpy.int32( len(nucleic_acid_list) )
        
        # --- list with the sizes from each chromossome
        cl_chromossome_size_list               = numpy.array( chromossome_size_list , dtype = numpy.int32 )
        
        # --- how many chromossome will be built
        cl_chromossome_max_size                = numpy.int32( max( chromossome_size_list ) )
        
        # --- devices ---
        
        cl_chromossome_size_list_device  = openCL.Buffer( self.context , openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR , hostbuf = cl_chromossome_size_list         )
        cl_chromossome_max_size_device   = openCL.Buffer( self.context , openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR , hostbuf = cl_chromossome_max_size          )       
       
        cl_nucleic_acid_list_device      = openCL.Buffer( self.context , openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR , hostbuf = cl_nucleic_acid_values_list      ) 
        cl_nucleic_acid_list_size_device = openCL.Buffer( self.context , openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR , hostbuf = cl_nucleic_acid_values_list_size )

        cl_initialized_chromossome_population_device  = openCL.Buffer( self.context , openCL.mem_flags.WRITE_ONLY | openCL.mem_flags.COPY_HOST_PTR , size = cl_initialized_chromossome_population.nbytes , hostbuf = cl_initialized_chromossome_population)
        
        # --- loading kernel
        
        program = openCL.Program( self.context , self.kernel ).build()
        
        queue = openCL.CommandQueue( self.context , properties = execution_mode )

        event = program.generate_initial_population(

                    queue , 
                    cl_chromossome_size_list.shape ,

                    cl_initialized_chromossome_population_device ,
                    cl_chromossome_size_list_device , 
                    cl_chromossome_max_size_device ,

                    cl_nucleic_acid_list_device , 
                    cl_nucleic_acid_list_size_device 
                )
        
        event.wait()
        
        openCL.enqueue_copy( queue , cl_initialized_chromossome_population , cl_initialized_chromossome_population_device )
        
        cl_chromossome_size_list_device.release()
        cl_chromossome_max_size_device.release()
        cl_nucleic_acid_list_device.release()
        cl_nucleic_acid_list_size_device.release()
        cl_initialized_chromossome_population_device.release()
        
        # --- cleaning zeros ---
        
        #return self.remove_zeros( cl_initialized_chromossome_population )
        
        print '\n+-------------------+', \
              '\n| return structs as |', \
              '\n+-------------------+--------------------'  , \
              '\n|\tcl_initialized_chromossome_population :' , type( cl_initialized_chromossome_population ), \
              '\n|\tcl_chromossome_size_list              :' , type( cl_chromossome_size_list              ), \
              '\n|\tcl_chromossome_max_size               :' , type( cl_chromossome_max_size               ), \
              '\n+----------------------------------------'
            
        return  ( cl_initialized_chromossome_population , cl_chromossome_size_list , cl_chromossome_max_size ) 

class FitnessEnhanced :

    def __init__( self , context , debug_mode=False ):

        self.context = context
        
        self.RMFLAGS = None
        self.WMFLAGS = None
        
        try :
            
            # better use CPU for debug kernels, for while! 
            # NVIDIA CUDA have some stuff for printf but its not time for cuda! <3
            
            if debug_mode :
            
                self.kernel = ''.join( open( 'lordran/kernels/CPU_DEBUG_RP_fitness.cl' ) )
        
                self.RMFLAGS = openCL.mem_flags.READ_ONLY  | openCL.mem_flags.USE_HOST_PTR
                self.WMFLAGS = openCL.mem_flags.WRITE_ONLY | openCL.mem_flags.USE_HOST_PTR
            
            else :
                
                self.RMFLAGS = openCL.mem_flags.READ_ONLY  | openCL.mem_flags.COPY_HOST_PTR 
                self.WMFLAGS = openCL.mem_flags.WRITE_ONLY | openCL.mem_flags.COPY_HOST_PTR
                self.kernel = ''.join( open( 'lordran/kernels/CPU_RP_fitness.cl' ) )
            
        except :
            
            print '[error] Some of this bitch (kernerl files) are not available!'
            
            exit( 0 )
        
    
    def execute ( self , execution_mode , chromossome_list , chromossome_offset_list , chromossome_max_size , puzzle ):
        
        cl_chromossome_list        = numpy.array( chromossome_list               , dtype=numpy.int32 )
        cl_chromossome_offset_list = numpy.array( chromossome_offset_list        , dtype=numpy.int32 )
        cl_fitness_results         = numpy.zeros( ( len( chromossome_list ) , 1) , dtype=numpy.int32 )
        
        #print '[python][FitnessEnhanced][setting up buffers]'
        
        cl_chromossome_list_device        = openCL.Buffer ( self.context , self.RMFLAGS , size = cl_chromossome_list.nbytes        , hostbuf = cl_chromossome_list )
        cl_chromossome_offset_list_device = openCL.Buffer ( self.context , self.RMFLAGS , size = cl_chromossome_offset_list.nbytes , hostbuf = cl_chromossome_offset_list )
        cl_fitness_results_device         = openCL.Buffer ( self.context , self.WMFLAGS , size = cl_fitness_results.nbytes         , hostbuf = cl_fitness_results )
        
        
        #~  _   __                     _  ______                                                          
        #~ | | / /                    | | | ___ \                                                         
        #~ | |/ /  ___ _ __ _ __   ___| | | |_/ / __ ___ _ __  _ __ ___   ___ ___  ___ ___  ___  _ __ ___ 
        #~ |    \ / _ \ '__| '_ \ / _ \ | |  __/ '__/ _ \ '_ \| '__/ _ \ / __/ _ \/ __/ __|/ _ \| '__/ __|
        #~ | |\  \  __/ |  | | | |  __/ | | |  | | |  __/ |_) | | | (_) | (_|  __/\__ \__ \ (_) | |  \__ \
        #~ \_| \_/\___|_|  |_| |_|\___|_| \_|  |_|  \___| .__/|_|  \___/ \___\___||___/___/\___/|_|  |___/
        #                                              | |                                               
        #                                              |_|                                               
        
        #print '[python][FitnessEnhanced][setting up kernel preprocessors]'
        
        problem_instance_itself = str( puzzle.instance ).replace('[' , '{').replace( ']' , '}' )
        
        side_factor = puzzle.side_factor
        
        bottom_left_index = puzzle.bottom_left_index

        # Passando os tamanhos dos arrays/matrizes
        
        self.kernel = self.kernel.replace( '[REPLACE_CHROMOSSOME_LIST_LINES]'             , str( len( chromossome_list ) )        )
        self.kernel = self.kernel.replace( '[REPLACE_CHROMOSSOME_LIST_COLUMNS]'           , str( chromossome_max_size )           )
        self.kernel = self.kernel.replace( '[REPLACE_CHROMOSSOME_OFFSET_LIST_LINES]'      , str( len( chromossome_offset_list ) ) )
        self.kernel = self.kernel.replace( '[REPLACE_CHROMOSSOME_MAXIMUM_SIZE]'           , str( chromossome_max_size )           )
        
        self.kernel = self.kernel.replace( '[REPLACE_PROBLEM_INSTANCE_SIZE]'              , str( puzzle.size )                    )
        self.kernel = self.kernel.replace( '[REPLACE_PROBLEM_INSTANCE_SIDE_FACTOR]'       , str( side_factor )                    )
        self.kernel = self.kernel.replace( '[REPLACE_PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX]' , str( bottom_left_index )              )
        self.kernel = self.kernel.replace( '[REPLACE_PROBLEM_INSTANCE]'                   , problem_instance_itself               )
        
        program = openCL.Program      ( self.context , self.kernel ).build()
        
        queue   = openCL.CommandQueue ( self.context , properties = execution_mode )
        
        event = program.fitness(
       
                    queue , 
       
                    cl_fitness_results.shape          ,
                    
                    cl_chromossome_list_device        ,
                    
                    cl_chromossome_offset_list_device ,
                    
                    cl_fitness_results_device         
                    
                    
                )
        
        event.wait()
        
        openCL.enqueue_copy( queue , cl_fitness_results , cl_fitness_results_device )
        
        print '[python][FitnessEnhanced][kernel execution is done]'
        
        return ( cl_fitness_results , cl_chromossome_list , cl_chromossome_offset_list )

# ---[END][FitnessEnhanced]-------------------------------------------------------------------------------------------------------------------------

class Crossover :

    def __init__( self , context , debug_mode=False ):
        
        self.context = context
        
        self.RMFLAGS = None
        self.WMFLAGS = None
        
        try :
            
            # better use CPU for debug kernels, for while! 
            # NVIDIA CUDA have some stuff for printf but its not time for cuda! <3
            
            if debug_mode :
            
                self.kernel = ''.join( open( 'lordran/kernels/CPU_DEBUG_RP_crossover.cl' ) )
        
                self.RMFLAGS = openCL.mem_flags.READ_ONLY  | openCL.mem_flags.USE_HOST_PTR
                self.WMFLAGS = openCL.mem_flags.WRITE_ONLY | openCL.mem_flags.USE_HOST_PTR
            
            else :
                
                self.RMFLAGS = openCL.mem_flags.READ_ONLY  | openCL.mem_flags.COPY_HOST_PTR 
                self.WMFLAGS = openCL.mem_flags.WRITE_ONLY | openCL.mem_flags.COPY_HOST_PTR
                self.kernel = ''.join( open( 'lordran/kernels/CPU_RP_crossover.cl' ) )
            
        except :
            
            print '[error] Some of this bitch (kernerl files) are not available!'
            
            exit( 0 ) 

    def execute( self , execution_mode , fitness_result_list , chromossome_list , chromossome_offset_list ):
        
        print '[python][crossover] building numpy structs'
        
        # --- building buffers ---
        
        print '[python][crossover] building buffers'
        
        cl_chromossome_list        = numpy.array( chromossome_list        , dtype=numpy.int32 )
        cl_chromossome_offset_list = numpy.array( chromossome_offset_list , dtype=numpy.int32 )
        cl_fitness_result_list     = numpy.array( fitness_result_list     , dtype=numpy.int32 )
        
        cl_new_chromossome_list    = numpy.zeros( ( chromossome_list.shape[0] , chromossome_list.shape[1] * 2 ) , dtype=numpy.int32 )

        print '[python][crossover] buffer status'

        print 'bgn_status[['
        
        print 'cl_chromossome_list        : ' , cl_chromossome_list.shape
        print 'cl_chromossome_offset_list : ' , cl_chromossome_offset_list.shape
        print 'fitness_result_list        : ' , cl_fitness_result_list.shape
        print 'cl_new_chromossome_list    : ' , cl_new_chromossome_list.shape

        print ']]end_status'
                
        # --- building devices -
        
        print '[python][crossover] building devices'

        cl_chromossome_list_device        = openCL.Buffer ( self.context , self.RMFLAGS , size = cl_chromossome_list.nbytes        , hostbuf = cl_chromossome_list        )
        cl_chromossome_offset_list_device = openCL.Buffer ( self.context , self.RMFLAGS , size = cl_chromossome_offset_list.nbytes , hostbuf = cl_chromossome_offset_list )
        cl_fitness_result_list_device     = openCL.Buffer ( self.context , self.RMFLAGS , size = cl_fitness_result_list.nbytes     , hostbuf = cl_fitness_result_list     ) 
        cl_new_chromossome_list_device    = openCL.Buffer ( self.context , self.WMFLAGS , size = cl_new_chromossome_list.nbytes    , hostbuf = cl_new_chromossome_list )

        # --- Adjusting Kernel Preprocessors ---
        
        self.kernel = self.kernel.replace('[REPLACE_NEW_CHROMOSSOME_LIST_COLUMN_LEN]' , str( cl_new_chromossome_list.shape[1] ) )
        self.kernel = self.kernel.replace('[REPLACE_OLD_CHROMOSSOME_LIST_COLUMN_LEN]' , str( cl_chromossome_list.shape[1] ) )
        self.kernel = self.kernel.replace('[REPLACE_FITNESS_LIST_LEN]'                , str( cl_fitness_result_list.shape[1] ) )
        
        # --- Loading kernel --- 

        print '[python][crossover] building kernel'

        program = openCL.Program      ( self.context , self.kernel ).build()
        
        print '[python][crossover] building queue'

        queue   = openCL.CommandQueue ( self.context , properties = execution_mode )
        
        print '[python][crossover] calling kernel'

        event = program.crossover(
       
                    queue , 
                    
                    cl_fitness_result_list.shape      ,
                    
                    cl_new_chromossome_list_device    ,

                    cl_chromossome_list_device        ,
                    
                    cl_chromossome_offset_list_device ,
                    
                    cl_fitness_result_list_device         
                    
                )
        
        event.wait()
        
        openCL.enqueue_copy( queue , cl_new_chromossome_list , cl_new_chromossome_list_device )

        print '[crossover] done ...'
        
        return 0



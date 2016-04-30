from lordran import platform_selector       as ps
from lordran import sliding_puzzle_parallel as spp

def init_pop( context , random_list , puzzle ):
    
    return spp.InitialPopulationGeneratorEnhanced( context ).execute( ps.Execution.ASYNC , random_list , [ -1 , puzzle.move_top , 1 , puzzle.move_bot ] )
    
if __name__ == '__main__' :
    
    #~ puzzle = spp.Puzzle( range( 9 ) )
    
    puzzle = spp.Puzzle( [1,0,2,3,4,5,6,7,8] )
    
    context = ps.get_intel_context()
    
    import time
   
    # --- INITIAL POPULATION ---

    population , offset_list , max_chromossome_size = init_pop( context , range(1,10) , puzzle )    
    
    # --- FITNESS ---
    
    a = time.time()
    
    fitness_result_list , chromossome_list , chromossome_offset_list = spp.FitnessEnhanced( context ).execute( ps.Execution.ASYNC , population , offset_list , max_chromossome_size , puzzle )
    
    # --- CROSSOVER ---
    
    print 'fitness_result_list:' , type( fitness_result_list )
    print 'chromossome_list:' , type( chromossome_list )
    print 'chromossome_offset_list:' , type( chromossome_offset_list )

    new_chromossome_list = spp.Crossover( context , True).execute( 0 , fitness_result_list , chromossome_list , chromossome_offset_list )

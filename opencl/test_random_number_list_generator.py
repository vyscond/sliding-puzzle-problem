from lordran import platform_selector       as ps
from lordran import sliding_puzzle_parallel as spp

def random_pop_size( context , how_many , max_size_chromossome ):
    
    print '[random list generator]'
    
    return spp.RandomNumberList( context ).execute( ps.Execution.ASYNC , how_many , max_size_chromossome )

    exit( 0 )

if __name__ == '__main__' :
     
    import time
    
    context = ps.get_intel_context()
    
    a = time.time()
    
    random_list = random_pop_size( context , 10  , 10 )
   
    a = time.time() - a
    
    print '-->[ Finish at : ' , ( a / 60 ) , ']'
	
    print random_list 

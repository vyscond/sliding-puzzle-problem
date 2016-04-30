
/*
+--------------+----------------------------+
| chr_l        | chromossome list           |
+--------------+----------------------------+
| fts_r        | fitness result             |
+--------------+----------------------------+
 */

/*

Lembra que vamos iterar sobre o 1-dimensional array of fitness
and not over the chromossome.

The iteration over the chromossome will be made into the kernel!

*/

#pragma OPENCL EXTENSION all : enable 

#define CHROMOSSOME_LIST_LINES [REPLACE_CHROMOSSOME_LIST_LINES]

#define CHROMOSSOME_LIST_COLUMNS [REPLACE_CHROMOSSOME_LIST_COLUMNS]

#define CHROMOSSOME_OFFSET_LIST_LINES [REPLACE_CHROMOSSOME_OFFSET_LIST_LINES]

#define CHROMOSSOME_MAXIMUM_SIZE [REPLACE_CHROMOSSOME_MAXIMUM_SIZE]

#define PROBLEM_INSTANCE_SIZE [REPLACE_PROBLEM_INSTANCE_SIZE]

#define PROBLEM_INSTANCE_SIDE_FACTOR [REPLACE_PROBLEM_INSTANCE_SIDE_FACTOR]

#define PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX [REPLACE_PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX]

#define PROBLEM_INSTANCE_BOTTOM_RIGHT_INDEX PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX + PROBLEM_INSTANCE_SIDE_FACTOR - 1

#define PROBLEM_INSTANCE_TOP_RIGHT_INDEX PROBLEM_INSTANCE_SIDE_FACTOR - 1

#define MOVE_TOP -PROBLEM_INSTANCE_SIDE_FACTOR

#define MOVE_BOT PROBLEM_INSTANCE_SIDE_FACTOR

void show_constant_status()
{
    printf("\n --------------------- MACRO STATUS --------------------- ");
    printf("\n PROBLEM_INSTANCE_SIZE               %i " , PROBLEM_INSTANCE_SIZE );
    printf("\n PROBLEM_INSTANCE_SIDE_FACTOR        %i " , PROBLEM_INSTANCE_SIDE_FACTOR );
    printf("\n PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX  %i " , PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX );
    printf("\n PROBLEM_INSTANCE_BOTTOM_RIGHT_INDEX %i " , PROBLEM_INSTANCE_BOTTOM_RIGHT_INDEX );
    printf("\n PROBLEM_INSTANCE_TOP_RIGHT_INDEX    %i " , PROBLEM_INSTANCE_TOP_RIGHT_INDEX );
    printf("\n MOVE_TOP                            %i " , MOVE_TOP );
    printf("\n MOVE_BOT                            %i " , MOVE_BOT );
    printf("\n --------------------- MACRO STATUS --------------------- \n\n");
}

int find_index_for_zero( int *problem_instance  )
{
    int x;
    for( x = 0 ; x < PROBLEM_INSTANCE_SIZE ; x++ )
    {
        if( *(problem_instance+x) == 0 )
        {
            //printf("\n\t\tfound zero = %i\n" , *(problem_instance+x) );
            return x;
        }
    }
    
    return -1;
}

int out_of_place( int *problem_instance  )
{
    int x ,  pieces_out_of_place_qtd;
    
    pieces_out_of_place_qtd = 0;
    
    for( x = 0 ; x < PROBLEM_INSTANCE_SIZE ; x++ )
    {
        if( *(problem_instance+x) != x )
        {
            //printf("\n\t\tfound zero = %i\n" , *(problem_instance+x) );
            pieces_out_of_place_qtd += 1;
        }
    }
    
    return pieces_out_of_place_qtd - 1;
}

int is_valid_move( int zero_index , int move )
{
    
    int i;
    
    //printf("\n\t\t\tNew index sum = [%i]" , (zero_index + move) );
    
    // MOVE ELEMENT FROM LEFT
    if( move == -1 )
    {
        //printf("\n\t[try to move left piece]");
        // canto superior esquerdo, ou canto inferior esquerdo
        if( (zero_index == 0) || ( zero_index == PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX ) )
        {
            return 0;
        }
        // demais indices da primeira coluna da esquerda
        else if( (zero_index % PROBLEM_INSTANCE_SIDE_FACTOR) == 0 )
        {
            return 0;
        }
    }

    else if( move == 1 )
    {
        //printf("\n\t[try to move right piece]");
        // canto superior direito, ou canto inferior direito
        if( zero_index == PROBLEM_INSTANCE_TOP_RIGHT_INDEX || zero_index == PROBLEM_INSTANCE_BOTTOM_RIGHT_INDEX ) 
        {
            return 0;
        }
        // demais indices da primeira coluna da direita
        else if( (zero_index % PROBLEM_INSTANCE_SIDE_FACTOR) == (PROBLEM_INSTANCE_SIDE_FACTOR - 1) )
        {
            return 0;
        }
    }

    else if( move == MOVE_TOP )
    {
        //printf("\n\t[try to move top piece]");
        //linha superior + cantos superiores
        if( (zero_index >= 0) && (zero_index <= PROBLEM_INSTANCE_TOP_RIGHT_INDEX) )

        {
            return 0;
        }                     
    }
   
    else if( move == MOVE_BOT )
    {
        //printf("\n\t[try to move bottom piece]");
        //linha inferior + cantos inferiores
        if( (zero_index >= PROBLEM_INSTANCE_BOTTOM_LEFT_INDEX ) && (zero_index <= PROBLEM_INSTANCE_BOTTOM_RIGHT_INDEX) )
        {
            return 0;
        }                     
    }
    
    return 1;
    
}

void show_stance( int *problem_instance )
{
    int j;
    
    printf("\n[" , problem_instance );
    
    for( j = 0 ; j < PROBLEM_INSTANCE_SIZE ; j++)
    {
        //if ( j % PROBLEM_INSTANCE_SIDE_FACTOR == 0 )
        //{
        //   printf("\n\t\t");
        //}
        
        printf ("%i " , *(problem_instance + j) );
    }
    
    printf("]\n");
}

__kernel void fitness
(
    __global int* chr_l ,
    __global int* offset_l,
    __global int* fts_r 
   
)
{
    int base_line_index , j;
    
    int problem_instance[] = [REPLACE_PROBLEM_INSTANCE] ;
    int moves_applied;
    int zero_index;
    int move;
    
    moves_applied = 0;
    
    base_line_index = get_global_id(0);
    
    /*-----------------------------------------------------------------------*
    
                               PRE-FITNESS PRESENTATION
    
     *-----------------------------------------------------------------------*/
    
    //printf("\n[Basic Configs are done] index [%i]\n" , base_line_index );
    
    //show_constant_status();
    
    //printf("\n\tChromossome for this instance -> [" );
    
    //for( j = 0 ; j < (*(offset_l + base_line_index)) ; j++)// ITERATING OVER THE SELECTED CHROMOSSOME
    //{
    //    printf (" %i " , *( ( chr_l+( base_line_index * CHROMOSSOME_MAXIMUM_SIZE) ) + j ) );
    //}
    
    //printf("]\n");
    
    //show_stance( problem_instance );
    
    /*-----------------------------------------------------------------------*
    
                        APPLYING CHROMOSSOME AS SOLUTION
    
     *-----------------------------------------------------------------------*/
    
    for( j = 0 ; j < (*(offset_l + base_line_index)) ; j++)// ITERATING OVER THE SELECTED CHROMOSSOME
    {
        
        zero_index = find_index_for_zero( problem_instance );
        
        // --- getting the next nucleic acid for the move test
        
        move = *( ( chr_l+( base_line_index * CHROMOSSOME_MAXIMUM_SIZE) ) + j );
        
        if( is_valid_move( zero_index , move ) ) // --- calculating the validation of the move ---
        {
            
            // --- applying the move
            
            //printf("\n\tMoving [%i] at index [%i] \n" , *( problem_instance + (zero_index + move)) , zero_index + move );
            
            // - simple swap <3
            *( problem_instance + zero_index ) = *( problem_instance + (zero_index + move)) ;
            *( problem_instance + (zero_index + move)) = 0;
            
            moves_applied += 1;
            
            //show_stance( problem_instance );
            
        }
        else
        {
            //printf("\n\t-- Its not a valid move | break loop --\n");
            
            break;
            // go to fitness
        }
    }
    
    //calc_fitness( moves_applied , moves_not_applied );
    
    //printf("\n\n\t\tThis is my final form\n");
    
    show_stance( problem_instance );
    
    printf( "\n\tout of place [%i]\n" , out_of_place( problem_instance ) );
    
    *(fts_r + base_line_index) = moves_applied;
    
    //printf("\n");
    
}




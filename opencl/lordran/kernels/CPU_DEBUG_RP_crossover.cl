
/*
    +----------------+-----------------------------+
    | n_chr_l        | new chromossomes list       |
    +----------------+-----------------------------+
    | o_chr_l        | old chromossomes list       |
    +----------------+-----------------------------+
    | o_chr_ofst_l   | old chromossome offset list |
    +----------------+-----------------------------+
    | ftn_l          | fitness list                |
    +----------------+-----------------------------+
 */

/* ---------------------------------- */

#define NEW_CHROMOSSOME_LIST_COLUMN_LEN [REPLACE_NEW_CHROMOSSOME_LIST_COLUMN_LEN]

#define OLD_CHROMOSSOME_LIST_COLUMN_LEN [REPLACE_OLD_CHROMOSSOME_LIST_COLUMN_LEN]

#define FITNESS_LIST_LEN [REPLACE_FITNESS_LIST_LEN]

/* ---------------------------------- 
 
 Nos vamos precisar do indices fixo de colunas pois invocares o kernel em modo de array!
 Isso fara com que possamos fazer o calculo cumulativo de fitness para a roleta!

*/

int* get_element( int i , int j )
{
    return (o_chr_l + (i * (o_chr_ofst_l + i) )) + j;
}

__kernel void crossover
(

    __global int* n_chr_l,
    __global int* o_chr_l,
    __global int* o_chr_ofst_l,
    __global int* ftn_l

)
{

    int base_line_index = get_global_id(0);
    
    int o_chr_row , o_chr_column ; //old chromossome I and J

    /* ----------------------------------------- */
    
    printf( "[opencl][crossover][%i][begin kernel execution]\n" , base_line_index );
    printf( "[opencl][crossover][%i][reding chromossome]" , base_line_index );
    for( o_chr_column = 0 ; o_chr_column < *(o_chr_ofst_l + base_line_index) ; o_chr_column++  )
    {
        printf( " %i " , get_element( base_line_index , o_chr_column ) );
    }
}


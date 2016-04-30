/*
   +--------------------------+-----------------------------+
   | chr_l                    | chromossome list            |
   +--------------------------+-----------------------------+
   | CHROMOSSOME_LIST_LEN     | length of chromossome list  |
   +--------------------------+-----------------------------+
   | CHROMOSSOME_MAXIMUM_SIZE | max size of an chromossome  |
   +--------------------------+-----------------------------+
   | nlc_ad_val_l             | nucleic acid list           |
   +--------------------------+-----------------------------+
   | NUCLEIC_ACID_LIST_LEN    | lenght of nucleic acid list |
   +--------------------------+-----------------------------+
 */

#define CHROMOSSOME_MAXIMUM_SIZE [REPLACE_CHROMOSSOME_MAXIMUM_SIZE]

#define NUCLEIC_ACID_LIST_LEN [REPLACE_NUCLEIC_ACID_LIST_LEN]

#define ELEMENT_ADDRESS ((chr_l+(line*CHROMOSSOME_MAXIMUM_SIZE))+column)

#define SEED ((((unsigned long) &line )+line)+column)

#define NUCLEIC_ACID_DRAWNED_INDEX ((SEED*SEED)%(65537*67777)%NUCLEIC_ACID_LIST_LEN)

#define CURRENT_OFFSET (*(offset_l + line))

__kernel void generate_initial_population
(
    __global int* chr_l        ,
    __global int* offset_l     ,
    __global int* nlc_ad_val_l   
)
{
    int line, column;
    
    line = get_global_id(0);
    
    column = get_global_id(1);
     
    if( CURRENT_OFFSET > column )
    {    
        printf( "[opencl][population_generator][testing new kernel] index[%i][%i] = [%i]\n" , line , column , *( nlc_ad_val_l +  NUCLEIC_ACID_DRAWNED_INDEX ) );
        
        *( ( chr_l+(line * CHROMOSSOME_MAXIMUM_SIZE) ) + column ) = *( nlc_ad_val_l +  NUCLEIC_ACID_DRAWNED_INDEX );
        
        // this line is supossed to be an:
        //
        // *(ELEMENT_ADDRESS) = *( ... )

    }

}


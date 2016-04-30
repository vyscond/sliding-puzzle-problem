#define UPPER_LIMIT [REPLACE_UPPER_LIMIT]
#define LOWERLIMIT [REPLACE_LOWER_LIMIT]

#define SEED ( ( (unsigned long) (&global_index) ) + global_index )

__kernel void random_number_list( __global int* drawn_numbers )
{
   int global_index = get_global_id(0);

   printf("\nglobal index = [%i]\n", global_index );

   *(drawn_numbers + global_index) = ( ( ( SEED * SEED ) % (65537 * 67777) ) % UPPER_LIMIT ) + LOWERLIMIT;
}

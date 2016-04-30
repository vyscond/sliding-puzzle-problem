import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

a = numpy.random.randn(4,4)

a = a.astype(numpy.int32)

a_gpu = cuda.mem_alloc(a.nbytes)

cuda.memcpy_htod(a_gpu, a)

mod = SourceModule("""
        
        #include <stdio.h>

        __global__ void doublify(int *a) { 
        
        int idx = threadIdx.x + threadIdx.y*4; a[idx] = 1;

        a[threadIdx.x][threadIdx.y] = 1;
        
        printf("( threadIdx.x , %i  ) | ( threadIdx.y , %i ) | ( idx , %i )  \\n" , threadIdx.x , threadIdx.y , idx);

        } """)

func = mod.get_function("doublify")
func(a_gpu, block=(4,4,1))

a_doubled = numpy.empty_like(a)
cuda.memcpy_dtoh(a_doubled, a_gpu)
print '\n'
print a_doubled
print a

from openalea.lpy import *
from string import ascii_uppercase
import psutil
from itertools import starmap 
lsystem = Lsystem('/home/begatim/Desktop/Thesis_Project/Practice/lpy_play/test.lpy')
"""
code = '''
Axiom:

production:
'''
for l,nl in zip(ascii_uppercase, ascii_uppercase[1:]+ascii_uppercase[0]):
    #code += l+' --> '+nl+'\n'
    code += l+''' : 
    for i in range(100):
        i+1
    produce '''+nl+'\n'
code += '\n'
#print(code)

lsystem.setCode(code)

lsystem.derive()

cores = psutil.cpu_count(logical=False)
cstring = lsystem.derive()
print("Length before parallel derivation",len(cstring))
partition_size = int(len(cstring)/cores)
res = None

if (len(cstring) % cores != 0):
    print("Entered the if inside the while loop")
    
    res = list(starmap(lsystem.partial_derivation,[(cstring,i*partition_size,partition_size  if i < cores-1 else partition_size + int(len(cstring) % cores)) for i in range(cores)]))
    print("Finished the computations")
else:
    print("Entered the else inside the while loop")
    res = list(starmap(lsystem.partial_derivation,[(cstring,i*partition_size, partition_size) for i in range(cores)]))
    print("Finished the computations")    

final_result = lsystem.AxialTree()

for i in range(len(res)):
    final_result += res[i]

print(len(final_result)) 
"""
updated_string = lsystem.parallel_iterate()
print(updated_string)

#print(lstring)
"""
def sequential_application(lstring, length):
    res = list(map(partial_application,[lstring[i*length:i*length+length] for i in range(len(ascii_uppercase))]))
    return res

def partial_application(lstring):
    return str(lsystem.iterate(Lstring(lstring)))

def parallel_application(lstring, length):
    from multiprocessing import Pool#, cpu_count
    cpu_count = psutil.cpu_count
    with Pool(cpu_count()) as p:
        res = list(p.imap(partial_application,[lstring[i*length:i*length+length] for i in range(len(ascii_uppercase))]))
        return res

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        length = int(sys.argv[1])
        lstring = ''.join([l*length for l in ascii_uppercase])
    else:
        length = 100000
        lstring = ''.join([l*length for l in ascii_uppercase])

    import time
    c = time.perf_counter()
    res1 = sequential_application(lstring, length)
    print('Sequential :',time.perf_counter()-c)
    c = time.perf_counter()
    res2 = parallel_application(lstring, length)
    from psutil import cpu_count
    print('Parallel ('+str(cpu_count())+') :',time.perf_counter()-c)
    #print(res1)
    #print(res2)
    assert res1 == res2
"""
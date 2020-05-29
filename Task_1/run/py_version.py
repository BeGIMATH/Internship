import time


def f(x):
    # for i in range(10000):
    x += 1
    return x


list_length = 10000
start = time.time()

mlist = [i for i in range(list_length)]
for j in range(10000):
    for i in range(list_length):
        mlist[i] = f(mlist[i])

# for i in range(list_length):
#    print(mlist[i])
elapsed_time = (time.time()-start)
print(elapsed_time)

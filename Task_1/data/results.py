import numpy as np 
import matplotlib.pyplot as plt 

cores = [4,8,16,32,64,128]
sequential_10000 = [64.8329,64.8329,64.8329,64.8329,64.8329,64.8329]
sequential_20000 = [122.733,122.733,122.733,122.733,122.733,122.733]
sequential_50000 = [304.018,304.018,304.018,304.018,304.018,304.018]

parallel_10000 = [26.6982,13.7335,7.77959,3.8142,2.47436,2.45874]
parallel_20000 = [50.7587,27.5067,16.0628, 7.42411,4.73475,4.25184]
parallel_50000 = [129.226,68.0201,38.7351,18.5864,12.028,10.1931]


labels = ['4','8', '16', '32', '64', '128']
x = np.arange(len(labels))
width = 0.3

fig, ax = plt.subplots()

rects1 = ax.bar(x - width, sequential_50000,width/3,label='seq-10000')
rects2 = ax.bar(x - 2*width/3, sequential_20000,width/3,label='seq-20000')
rects3 = ax.bar(x - width/3, sequential_10000,width/3,label='seq-50000')
rects4 = ax.bar(x , parallel_50000,width/3,label='parallel-50000')
rects5 = ax.bar(x + width/3, parallel_20000,width/3,label='parallel-20000')
rects5 = ax.bar(x + 2*width/3, parallel_10000,width/3,label='parallel-10000')



# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Seconds')
ax.set_xlabel('Workers')
ax.set_title('Running time for a list of length 10000')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


plt.show()

"""
plt.plot(cores,best_fit_paper_100000_up,label="best-fit-bottom-up")
plt.plot(cores,best_fit_paper_100000_down,label="best-fit-top-down")

plt.plot(cores,first_fit_paper_100000_up,label="first-fit-bottom-up")
plt.plot(cores,first_fit_paper_100000_down,label="first-fit-top-down")

plt.plot(cores,best_fit_queue_100000_up,label="best-fit-queue-bottom-up")
plt.plot(cores,best_fit_queue_100000_down,label="best-fit-queue-top-down")

plt.plot(cores,best_fit_level_100000_up,label="best-fit-level-bottom-up")
plt.plot(cores,best_fit_level_100000_down,label="best-fit-level-top-down")
plt.grid(True)
plt.title("Timmings for 100000 nodes")
plt.legend()
plt.xlabel("Workers")
plt.ylabel("Time")
plt.show()

#Plot for 1000000 nodes

#plt.plot(cores,best_fit_paper_1000000_up,label="best-fit-bottom-up")
#plt.plot(cores,best_fit_paper_1000000_down,label="best-fit-top-down")

plt.plot(cores,first_fit_paper_1000000_up,label="first-fit-bottom-up")
plt.plot(cores,first_fit_paper_1000000_down,label="first-fit-top-down")

plt.plot(cores,best_fit_queue_1000000_up,label="best-fit-queue-bottom-up")
plt.plot(cores,best_fit_queue_1000000_down,label="best-fit-queue-top-down")

plt.plot(cores,best_fit_level_1000000_up,label="best-fit-level-bottom-up")
plt.plot(cores,best_fit_level_1000000_down,label="best-fit-level-top-down")
plt.grid(True)
plt.title("Timmings for 1000000 nodes")
plt.legend()
plt.xlabel("Workers")
plt.ylabel("Time")
plt.show()
"""
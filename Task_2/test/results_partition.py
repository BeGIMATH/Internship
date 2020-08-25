import numpy as np 
import matplotlib.pyplot as plt
best_fit_partition_time = [13.033053684,18.882497717999996,26.407995256999982,52.87286669899993,85.88166089899994]
first_fit_partition_time = [4.503660776999993,4.201578665999989,3.856527950000043,3.88718006900001,4.137125637000054]
best_fit_queue_partition_time = [3.936560727,4.536439862000009,6.756693721999966,10.329983804999983, 16.19789376999995]
best_fit_level_partition_time = [2.8586300719999826,2.6822470090000365,2.6830415800000083,3.2867700730000706,4.068576721999989]


cores = [8,16,32,64,128]



labels = ['8', '16', '32', '64', '128']
x = np.arange(len(labels))
width = 0.3

fig, ax = plt.subplots()

rects1 = ax.bar(x - width, best_fit_partition_time,width/2,label='Algo_1-best-fit')
rects2 = ax.bar(x - width/2, first_fit_partition_time,width/2,label='Algo_1-first-fit')
rects3 = ax.bar(x , best_fit_queue_partition_time,width/2,label='Algo_2')
rects4 = ax.bar(x + width/2, best_fit_level_partition_time,width/2,label='Algo_3')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')



# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Seconds')
ax.set_xlabel('Workers')
ax.set_title('Partitioning time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


plt.show()

import numpy as np 
import matplotlib.pyplot as plt
best_fit_bottom_up_time = [25.135173353,18.589709862999996,8.226164754000024, 9.88480016699998,3.97598286799996]
first_fit_bottom_up_time = [39.84485862000001,29.607937579999998, 22.465992420999953,16.001728274000016, 11.808462670999916]
best_fit_queue_bottom_up_time = [15.721866110999997,12.735350046999997,5.827673078000032,3.3987718590000213,11.082102427999985]
best_fit_level_bottom_up_time = [16.059789266999985,9.480483725,6.786624635999999,3.810705545000019, 2.896379711999998]


cores = [8,16,32,64,128]



labels = ['8', '16', '32', '64', '128']
x = np.arange(len(labels))
width = 0.3

fig, ax = plt.subplots()

rects1 = ax.bar(x - width,best_fit_bottom_up_time,width/2,label='Algo_1-best-fit')
rects2 = ax.bar(x - width/2,first_fit_bottom_up_time,width/2,label='Algo_1-first-fit')
rects3 = ax.bar(x ,best_fit_queue_bottom_up_time,width/2,label='Algo_2')
rects4 = ax.bar(x + width/2,best_fit_level_bottom_up_time,width/2,label='Algo_3')

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
ax.set_title('Bottom up traversal time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


plt.show()

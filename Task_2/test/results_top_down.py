import numpy as np 
import matplotlib.pyplot as plt
best_fit_top_down_time = [24.040147781, 15.94171940000001, 8.595817087, 5.420663452999975, 2.8879914730000564]
first_fit_top_down_time = [ 35.94707106,29.597883896999974, 22.646202098999993,18.96882364399994,15.889292481999973]
best_fit_queue_top_down_time = [15.565582525999986,12.184477148999974,5.510104634000015, 2.7820331870000246,1.8124813619999713]
best_fit_level_top_down_time = [15.944213421, 7.957303453999998, 5.59451022199994,3.1314507790000334,1.9250482209999973]

cores = [8,16,32,64,128]



labels = ['8', '16', '32', '64', '128']
x = np.arange(len(labels))
width = 0.3

fig, ax = plt.subplots()

rects1 = ax.bar(x - width,best_fit_top_down_time,width/2,label='Algo_1-best-fit')
rects2 = ax.bar(x - width/2,first_fit_top_down_time,width/2,label='Algo_1-first-fit')
rects3 = ax.bar(x ,best_fit_queue_top_down_time,width/2,label='Algo_2')
rects4 = ax.bar(x + width/2,best_fit_level_top_down_time,width/2,label='Algo_3')

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
ax.set_title('Top down traversal time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


plt.show()

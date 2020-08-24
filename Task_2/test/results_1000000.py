import numpy as np 
import matplotlib.pyplot as plt 

cores = [8,16,32,64,128]


best_fit_paper_100000_up = [40.931996622,37.263688625999976,41.208626030999994,58.00581150400001,92.61669829300001]

best_fit_paper_100000_down = [33.32370357,36.42942996400001,43.545262949000005,55.76935568100009,92.97985204200006]


best_fit_paper_1000000_up = [389.16008324100017,390.51068498600034,608.1262996099995,757.232195341001,1282.7485931049996]

best_fit_paper_1000000_down = [291.6045787029998,337.1282859230005,501.5493403800001,783.3000763170003 ,1279.1154010789996]



first_fit_paper_100000_down = [46.632376205,34.67271796299997,31.711196322999967,29.647773613000027,20.520630224000115]

first_fit_paper_100000_up = [21.03943914300001,17.155671864999988,14.453081240000074,12.450553549000006,11.303104843000028]


first_fit_paper_1000000_down = [361.19903007400035, 398.435528168, 313.3524456490004, 270.7497116119994, 223.01272640000025]

first_fit_paper_1000000_up = [273.419795541 , 202.449976375, 176.07519115299965, 154.9531804170001, 133.9491607359996]



best_fit_queue_100000_down = [32.072533108000016,12.630637121999996,10.90014364000001,10.561369075000016,13.285145956000179]

best_fit_queue_100000_up = [32.62700435299999,12.566795973000012,11.198037967000005,11.671412478000093,13.344368589000169]



best_fit_queue_1000000_down = [238.03475584100033,145.77302317799968,105.17675325599976,150.89627929000017,186.61464464799974]

best_fit_queue_1000000_up = [233.29998144899992,141.95748706499944, 107.20018065000022,166.31241986799978,194.96443122399978]



best_fit_level_100000_down = [20.023672087000023,11.947442734999981,8.335384775999955,6.897905371999968,5.899398277000046]

best_fit_level_100000_up = [18.872659139999996,11.830435320999982,8.435619598000017,6.210292942000024,6.108222038999884]




best_fit_level_1000000_down = [249.06465705200026,118.36405907600056,91.19626253299975,73.61626575599985,72.20256524300021]

best_fit_level_1000000_up = [246.36033302600026,128.27773336300015,91.06352961300036,91.47868681199907, 71.75412331400003]

labels = ['8', '16', '32', '64', '128']
x = np.arange(len(labels))
width = 0.3

fig, ax = plt.subplots()

rects1 = ax.bar(x - width, best_fit_paper_1000000_up,width/4,label='Algo_1-best-fit-bottom-up')
rects2 = ax.bar(x - 3*width/4, best_fit_paper_1000000_down,width/4,label='Algo_1-best-fit-top-down')
rects3 = ax.bar(x - width/2, first_fit_paper_1000000_up,width/4,label='Algo_1-first-fit-bottom-up')
rects4 = ax.bar(x - width/4, first_fit_paper_1000000_down,width/4,label='Algo_1-first-fit-top-down')
rects5 = ax.bar(x , best_fit_queue_1000000_up,width/4,label='Algo_2-bottom-up')
rects6 = ax.bar(x + width/4, best_fit_queue_1000000_down,width/4,label='Algo_2-top-down')
rects7 = ax.bar(x + width/2, best_fit_level_1000000_up,width/4,label='Algo_3-bottom-up')
rects8 = ax.bar(x + 3*width/4, best_fit_level_1000000_down,width/4,label='Algo_3-top-down')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Seconds')
ax.set_xlabel('Workers')
ax.set_title('Running time for a tree with 1000000 nodes')
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
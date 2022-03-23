import pickle
import matplotlib.pyplot as plt


def mean_value(list):
    return sum(list)/len(list)


with open("combined_emv_waiting_time.txt", "rb") as fp:
    emv_wt_fuzzy = pickle.load(fp)

a = emv_wt_fuzzy[:500]

mean_wmv_wt = mean_value(emv_wt_fuzzy)
print('avg_emv_wt')
print(mean_wmv_wt)

with open("combined_emv_waiting_time_no-fuzz.txt", "rb") as fp:
    emv_wt = pickle.load(fp)
b = emv_wt[:500]


mean_wmv_wt_no_fuz = mean_value(emv_wt)
print('avg_emv_wt no fuz')
print(mean_wmv_wt_no_fuz)

# xaxis = []
# i = 0
# while i < 500:
#     xaxis.append(i)
#     i += 1

plt.plot(a, label = "emergency vehicle waiting time in fuzzy controlled traffic")

plt.plot(b, label = "emergency vehicle waiting time fixed time traffic controller")

# naming the x axis
plt.xlabel('Time Step')
# naming the y axis
plt.ylabel('Waiting Time')

# giving a title to my graph
plt.title('Emergency vehicle waiting time comparism')

plt.legend()

# function to show the plot
plt.show()

# print("emv fuzz length")
# print(len(emv_wt_fuzzy))
#
# print("emv ordinary length")
# print(len(emv_wt));
#
# print("x axis length")
# print(len(xaxis))
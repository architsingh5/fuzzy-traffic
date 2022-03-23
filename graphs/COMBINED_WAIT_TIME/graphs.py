import pickle
import matplotlib.pyplot as plt


def mean_value(list):
    return sum(list)/len(list)


with open("vehicles_waiting_time.txt", "rb") as fp:
    vehicle_wt_count_fuzzy = pickle.load(fp)

mean_no_fuz = mean_value(vehicle_wt_count_fuzzy)
print('mean-no-fuz')
print(mean_no_fuz)

a = vehicle_wt_count_fuzzy[:500]


with open("vehicles_waiting_time_no-fuzz.txt", "rb") as fp:
    vehicle_count_no_fuzzy = pickle.load(fp)

b = vehicle_count_no_fuzzy[:500]

mean_fuz = mean_value(vehicle_count_no_fuzzy)
print('mean-fuz')
print(mean_fuz)


# i = 0
# while i < 500:
#     xaxis.append(i)
#     i += 1

plt.plot(a, label = "Fuzzy logic controlled traffic")

plt.plot(b, label = "Fixed time controlled traffic")

# naming the x axis
plt.xlabel('Time Step')
# naming the y axis
plt.ylabel('Waiting time')

# giving a title to my graph
plt.title('Combined Vehicle Waiting Time')

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
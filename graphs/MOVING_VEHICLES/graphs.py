import pickle
import matplotlib.pyplot as plt


def mean_value(list):
    return sum(list)/len(list)


with open("amount_moving_vehicles.txt", "rb") as fp:
    vehicle_count_fuzzy = pickle.load(fp)

a = vehicle_count_fuzzy[:500]


mean_vc_fuzzy = mean_value(vehicle_count_fuzzy)
print('avg_vc_fuzzy')
print(mean_vc_fuzzy)


with open("amount_moving_vehicles_no-fuzz.txt", "rb") as fp:
    vehicle_count_no_fuzzy = pickle.load(fp)

b = vehicle_count_no_fuzzy[:500]


mean_vc = mean_value(vehicle_count_no_fuzzy)
print('avg_vc')
print(mean_vc)


# i = 0
# while i < 500:
#     xaxis.append(i)
#     i += 1

plt.plot(a, label = "Fuzzy logic controlled traffic")

plt.plot(b, label = "Fixed time controlled traffic")

# naming the x axis
plt.xlabel('Time Step')
# naming the y axis
plt.ylabel('Number of vehicles')

# giving a title to my graph
plt.title('Amount of moving vehicles per time step')

plt.legend()

# function to show the plot
plt.show()
#
# # print("emv fuzz length")
# # print(len(emv_wt_fuzzy))
# #
# # print("emv ordinary length")
# # print(len(emv_wt));
# #
# # print("x axis length")
# # print(len(xaxis))
import pickle
import matplotlib.pyplot as plt

# with open("vehicles_waiting_time.txt", "rb") as fp:
#     vehicle_wt_count_fuzzy = pickle.load(fp)
#
# a = vehicle_wt_count_fuzzy[:500]
#
#
# with open("vehicles_waiting_time_no-fuzz.txt", "rb") as fp:
#     vehicle_count_no_fuzzy = pickle.load(fp)
#
# b = vehicle_count_no_fuzzy[:500]


# i = 0
# while i < 500:
#     xaxis.append(i)
#     i += 1

avg_vehicle_waiting_time = [988.91, 1199.58, 1308.71, 1658.60]
avg_emergency_vehicle_waiting_time = [0.075, 0.319, 0.586, 1.6]

plt.plot(avg_vehicle_waiting_time, label="Average vehicle waiting time")

plt.plot(avg_emergency_vehicle_waiting_time, label="Average emergency vehicle waiting time")

plt.plot(avg_emergency_vehicle_waiting_time_ftc, label="average vehicle waiting time (Fixed time Controller)")

plt.plot(avg_vehicle_waiting_time_ftc, label="Average emergency vehicle waiting time (Fixed time controller)")

# naming the x axis
plt.xlabel('Yellow Light Time (s)')
# naming the y axis

plt.ylabel('Average waiting time (s)')

# giving a title to my graph
plt.title('Average waiting time of vehicles for each yellow time')

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
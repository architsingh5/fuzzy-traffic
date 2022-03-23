import pickle
import matplotlib.pyplot as plt

labels = ['SUMO Fixed Time Traffic Controller', 'Fuzzy Logic Traffic Controller']
avg_vehicle_waiting_time = [405.4233864541833, 303.57359397001574]
# avg_emv_waiting_time = [3.68734375, 0.8426875]



width = 0.5

fig, ax = plt.subplots()

ax.bar(labels, avg_vehicle_waiting_time, width, label='Avg vehicle waiting time')
# ax.bar(labels, avg_emv_waiting_time, width,  bottom=avg_vehicle_waiting_time,
#       label='Avg Emergency vehicle waiting time')

ax.set_ylabel('Time (s)')
ax.set_title('Waiting time by controller and vehicle type')
ax.legend()

plt.show()



# # ########################
#


# import pickle
# import matplotlib.pyplot as plt
#
# labels = ['SUMO Fixed Time Traffic Controller', 'Fuzzy Logic Traffic Controller']
# # avg_vehicle_waiting_time = [405.4233864541833, 303.57359397001574]
# avg_emv_waiting_time = [3.68734375, 0.8426875]
#
#
#
# width = 0.5
#
# fig, ax = plt.subplots()
#
# # ax.bar(labels, avg_vehicle_waiting_time, width, label='Avg vehicle waiting time')
# ax.bar(labels, avg_emv_waiting_time, width,
#        label='Avg Emergency vehicle waiting time', color=['green'])
# # ax.color('orange')
# ax.set_ylabel('Time (s)')
# ax.set_title('Waiting time by controller and vehicle type')
# ax.legend()
#
# plt.show()
#
#
#
#

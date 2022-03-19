from collections import deque
from random import random
from threading import Thread
import time
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

queue_length = ctrl.Antecedent(np.arange(0,31,1), 'queue_length')
waiting_time = ctrl.Antecedent(np.arange(0,31,1), 'waiting_time')
greenSignalTime = ctrl.Consequent(np.arange(0,21,1), 'greenSignalTime')

level = ['low', 'medium', 'high']

queue_length.automf(3, names=level)
waiting_time.automf(3, names=level)
greenSignalTime.automf(3, names=level)

rule1 = ctrl.Rule(queue_length['low'] & waiting_time['low'], greenSignalTime['low'])
rule2 = ctrl.Rule(queue_length['low'] & waiting_time['medium'], greenSignalTime['medium'])
rule3 = ctrl.Rule(queue_length['low'] & waiting_time['high'], greenSignalTime['high'])
rule4 = ctrl.Rule(queue_length['medium'] & waiting_time['low'], greenSignalTime['low'])
rule5 = ctrl.Rule(queue_length['medium'] & waiting_time['medium'], greenSignalTime['medium'])
rule6 = ctrl.Rule(queue_length['medium'] & waiting_time['high'], greenSignalTime['high'])
rule7 = ctrl.Rule(queue_length['high'] & waiting_time['low'], greenSignalTime['low'])
rule8 = ctrl.Rule(queue_length['high'] & waiting_time['medium'], greenSignalTime['medium'])
rule9 = ctrl.Rule(queue_length['high'] & waiting_time['high'], greenSignalTime['high'])

GST_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

GST_control_sim = ctrl.ControlSystemSimulation(GST_control)

id = 0
number_of_vehicles_crossed_in_static=0
number_of_vehicles_crossed_in_dynamic=0
flag = 0
total_waiting_time_in_static = 0
total_waiting_time_in_dynamic = 0


class Vehicle:
    def __init__(self, id):
        self.id = id
        self.start_time = time.time()
        self.end_time = 0
        self.waiting_time = 0


lane0_static = deque()
lane1_static = deque()
lane2_static = deque()
lane3_static = deque()
lane0_dymanic = deque()
lane1_dymanic = deque()
lane2_dymanic = deque()
lane3_dymanic = deque()
static_exit_list = []
dynamic_exit_list = []

start_time = time.time()

def random_vehicle_generator(time_interval):
    global lane0_static, lane1_static, lane2_static, lane3_static, id, flag
    global lane0_dymanic, lane1_dymanic, lane2_dymanic, lane3_dymanic
    while True:
        t = random()
        if t > 0.5:
            lane = random()
            if lane < 0.25:
                lane0_static.append(Vehicle(id))
                lane0_dymanic.append(Vehicle(id))
            elif lane < 0.5:
                lane1_static.append(Vehicle(id))
                lane1_dymanic.append(Vehicle(id))
            elif lane < 0.75:
                lane2_static.append(Vehicle(id))
                lane2_dymanic.append(Vehicle(id))
            else:
                lane3_static.append(Vehicle(id))
                lane3_dymanic.append(Vehicle(id))
            id += 2
            time.sleep(random()*3)
        else:
            time.sleep(random()*3)
        if time.time() - start_time >  time_interval:
            flag = 1
            break

def opening_lanes_in_static(time_interval):
    global lane0_static, lane1_static, lane2_static, lane3_static, number_of_vehicles_crossed_in_static, total_waiting_time_in_static
    while True:
        for i in range(4):
            curr_time = time.time()
            # print('Static: Lane {} opened for {} seconds'.format(i,time_interval))
            while time.time() - curr_time < time_interval:
                
                if i == 0:
                    if len(lane0_static) > 0:
                        # print('Vehicle {} gets out from lane {}'.format(lane0_static[0].id, i))
                        outvehicle = lane0_static.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_static += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_static=number_of_vehicles_crossed_in_static+1
                        static_exit_list.append(outvehicle)
                        
                elif i == 1:
                    if len(lane1_static) > 0:
                        # print('Vehicle {} gets out from lane {}'.format(lane1_static[0].id, i))
                        outvehicle = lane1_static.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_static += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_static=number_of_vehicles_crossed_in_static+1
                        static_exit_list.append(outvehicle)

                elif i == 2:
                    if len(lane2_static) > 0:
                        # print('Vehicle {} gets out from lane {}'.format(lane2_static[0].id, i))
                        outvehicle = lane2_static.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_static += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_static=number_of_vehicles_crossed_in_static+1
                        static_exit_list.append(outvehicle)

                elif i == 3:
                    if len(lane3_static) > 0:
                        # print('Vehicle {} gets out from lane {}'.format(lane3_static[0].id, i))
                        outvehicle = lane3_static.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_static += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_static=number_of_vehicles_crossed_in_static+1
                        static_exit_list.append(outvehicle)

                if flag == 1:
                    break

                time.sleep(0.8)

            # print('Static: Lane {} closed:'.format(i))
        
            if flag == 1:
                break

        if flag == 1:
            break


def opening_lanes_in_dymanic():
    global time_to_open, lane0_dymanic, lane1_dymanic, lane2_dymanic, lane3_dymanic, number_of_vehicles_crossed_in_dynamic, total_waiting_time_in_dynamic
    while True:
        for i in range(4):
            curr_time = time.time()
            if i == 0:
                max_waiting_time = 0
                if len(lane0_dymanic) > 0:
                    lane0_dymanic[0].waiting_time = curr_time - lane0_dymanic[0].start_time
                    max_waiting_time = lane0_dymanic[0].waiting_time
                
                calculate_time_to_open(len(lane0_dymanic), max_waiting_time)

                time_for_gst = max(time_to_open, 2)

                # print("Dynamic: Lane {} opened for {} seconds".format(i, time_for_gst))
                
                while time.time() - curr_time < time_for_gst:

                    if len(lane0_dymanic) > 0:
                        # print('Vehicle {} gets out from lane {}'.format(lane0_dymanic[0].id, i))
                        outvehicle = lane0_dymanic.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_dynamic += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_dynamic=number_of_vehicles_crossed_in_dynamic+1
                        dynamic_exit_list.append(outvehicle)
                        time.sleep(0.8)


                # print('Dynamic: Lane {} closed:'.format(i))


            elif i == 1:
                max_waiting_time = 0
                if len(lane1_dymanic) > 0:
                    lane1_dymanic[0].waiting_time = curr_time - lane1_dymanic[0].start_time
                    max_waiting_time = lane1_dymanic[0].waiting_time
                
                calculate_time_to_open(len(lane1_dymanic), max_waiting_time)

                time_for_gst = time_to_open

                # print("Dynamic: Lane {} opened for {} seconds".format(i, time_for_gst))
                
                while time.time() - curr_time < time_for_gst:

                    if len(lane1_dymanic) > 0:
                        # print('Vehicle {} gets out from lane {}'.format(lane1_dymanic[0].id, i))
                        outvehicle = lane1_dymanic.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_dynamic += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_dynamic=number_of_vehicles_crossed_in_dynamic+1
                        dynamic_exit_list.append(outvehicle)
                        time.sleep(0.8)

                # print('Dynamic: Lane {} closed:'.format(i))

            elif i == 2:
                max_waiting_time = 0
                if len(lane2_dymanic) > 0:
                    lane2_dymanic[0].waiting_time = curr_time - lane2_dymanic[0].start_time
                    max_waiting_time = lane2_dymanic[0].waiting_time
                
                calculate_time_to_open(len(lane2_dymanic), max_waiting_time)

                time_for_gst = time_to_open
                    
                # print("Dynamic: Lane {} opened for {} seconds".format(i, time_for_gst))

                while time.time() - curr_time < time_for_gst:

                    if len(lane2_dymanic) > 0:

                        # print('Vehicle {} gets out from lane {}'.format(lane2_dymanic[0].id, i))
                        outvehicle = lane2_dymanic.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_dynamic += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_dynamic=number_of_vehicles_crossed_in_dynamic+1
                        dynamic_exit_list.append(outvehicle)
                        time.sleep(0.8)

                # print('Dymanic: Lane {} closed'.format(i))

            elif i == 3:
                max_waiting_time = 0
                if len(lane3_dymanic) > 0:
                    lane3_dymanic[0].waiting_time = curr_time - lane3_dymanic[0].start_time
                    max_waiting_time = lane3_dymanic[0].waiting_time
                
                calculate_time_to_open(len(lane3_dymanic), max_waiting_time)

                time_for_gst = time_to_open
                    
                # print("Lane {} opened for {} seconds".format(i, time_for_gst))

                while time.time() - curr_time < time_for_gst:

                    if len(lane3_dymanic) > 0:
                        # print('Vehicle {} gets out from lane {}'.format(lane3_dymanic[0].id, i))
                        outvehicle = lane3_dymanic.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time_in_dynamic += outvehicle.waiting_time
                        number_of_vehicles_crossed_in_dynamic=number_of_vehicles_crossed_in_dynamic+1
                        dynamic_exit_list.append(outvehicle)
                        time.sleep(0.8)

                # print('Lane {} closed'.format(i))

            if flag == 1:
                break
        if flag == 1:
            break

def static_traffic_light_system():
    opening_lanes_in_static(20)
    print('Total number of vehicles crossed in static: {}'.format(number_of_vehicles_crossed_in_static))
    print('Total waiting time in static: {}'.format(round(total_waiting_time_in_static, 2)))
    print('Average waiting time in static: {}'.format(round(total_waiting_time_in_static/number_of_vehicles_crossed_in_static,2)))
    print('Total time in static: {}'.format(round(time.time() - start_time,2)))

time_to_open = 0

def calculate_time_to_open(queue_length, maximumWaitingTime):
    global time_to_open
    GST_control_sim.input['queue_length'] = queue_length
    GST_control_sim.input['waiting_time'] = maximumWaitingTime
    GST_control_sim.compute()
    time_to_open = round(GST_control_sim.output['greenSignalTime'],2)

def dynamic_traffic_light_system():
    opening_lanes_in_dymanic()
    print('Total number of vehicles crossed in dynamic: {}'.format(number_of_vehicles_crossed_in_dynamic))
    print('Total waiting time in dynamic: {}'.format(round(total_waiting_time_in_dynamic, 2)))
    print('Average waiting time in dynamic: {}'.format(round(total_waiting_time_in_dynamic/number_of_vehicles_crossed_in_dynamic,2)))
    print('Total time in dynamic: {}'.format(round(time.time() - start_time,2)))


if __name__ == '__main__':

    print("This code is not optimised yet and may produce irrevelant results")
    print("Wait around 120 seconds for the simulation to complete")

    t1 = Thread(target=random_vehicle_generator, args=(120,))
    t2 = Thread(target=static_traffic_light_system,)
    t3 = Thread(target=dynamic_traffic_light_system,)
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    x=[]
    y1 = []
    y2 = []

    for i in range(id):
        x.append(i)
        flag1 =0 
        flag2 =0
        for vehicle in static_exit_list:
            if vehicle.id == i:
                y1.append(vehicle.waiting_time)
                flag1 = 1
                break
        if flag1 == 0:
            y1.append(0)
        for vehicle in dynamic_exit_list:
            if vehicle.id == i:
                y2.append(vehicle.waiting_time)
                flag2 = 1
                break
        if flag2 == 0:
            y2.append(0)

    plt.bar(x, y1, label='Static')
    plt.bar(x, y2, label='Dynamic')
    plt.xlabel('Vehicle ID')
    plt.ylabel('Waiting Time')
    plt.title('Waiting Time vs Vehicle ID')
    plt.legend()
    plt.show()
    
from collections import deque
from random import random
from threading import Thread
import time

id = 0
number_of_vehicles_crossed=0
flag = 0
total_waiting_time = 0

class Vehicle:
    def __init__(self, id):
        self.id = id
        self.start_time = time.time()
        self.end_time = 0
        self.waiting_time = 0

start_time = time.time()

lane0 = deque()
lane1 = deque()
lane2 = deque()
lane3 = deque()

def random_vehicle_generator():
    global lane0, lane1, lane2, lane3, id, flag
    while True:
        t = random()
        if t > 0.5:
            lane = random()
            if lane < 0.25:
                lane0.append(Vehicle(id))
            elif lane < 0.5:
                lane1.append(Vehicle(id))
            elif lane < 0.75:
                lane2.append(Vehicle(id))
            else:
                lane3.append(Vehicle(id))
            id += 1
            time.sleep(1)
        if time.time() - start_time > 120:
            flag = 1
            break


def opening_lanes():
    global lane0, lane1, lane2, lane3, number_of_vehicles_crossed, total_waiting_time
    while True:
        for i in range(4):
            curr_time = time.time()
            print('Lane {} opened:'.format(i))
            while time.time() - curr_time < 10:
                
                if i == 0:
                    if len(lane0) > 0:
                        print('Vehicle {} gets out from lane {}'.format(lane0[0].id, i))
                        outvehicle = lane0.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time += outvehicle.waiting_time
                elif i == 1:
                    if len(lane1) > 0:
                        print('Vehicle {} gets out from lane {}'.format(lane1[0].id, i))
                        outvehicle = lane1.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time += outvehicle.waiting_time
                elif i == 2:
                    if len(lane2) > 0:
                        print('Vehicle {} gets out from lane {}'.format(lane2[0].id, i))
                        outvehicle = lane2.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time += outvehicle.waiting_time
                elif i == 3:
                    if len(lane3) > 0:
                        print('Vehicle {} gets out from lane {}'.format(lane3[0].id, i))
                        outvehicle = lane3.popleft()
                        outvehicle.end_time = time.time()
                        outvehicle.waiting_time = outvehicle.end_time - outvehicle.start_time
                        total_waiting_time += outvehicle.waiting_time

                
                number_of_vehicles_crossed=number_of_vehicles_crossed+1

                if flag == 1:
                    break

                time.sleep(0.8)

            print('Lane {} closed:'.format(i))
        
            if flag == 1:
                break

        if flag == 1:
            break

def static_traffic_light_system():
    t1 = Thread(target=random_vehicle_generator)
    t2 = Thread(target=opening_lanes)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


    print('Total number of vehicles crossed: {}'.format(number_of_vehicles_crossed))
    print('Total waiting time: {}'.format(round(total_waiting_time, 2)))
    print('Average waiting time: {}'.format(round(total_waiting_time/number_of_vehicles_crossed,2)))
    print('Total time: {}'.format(round(time.time() - start_time,2)))

def dynamic_traffic_light_system():
    pass

if __name__ == '__main__':
    static_traffic_light_system()


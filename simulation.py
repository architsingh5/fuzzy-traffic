from simulation_static import static_tls
from simulation_dynamic import dynamic_tls

if __name__ == "__main__":
    print("===STATIC===")
    a1,b1,c1,d1 = static_tls()
    print()
    print("===DYNAMIC===")
    a2,b2,c2,d2 = dynamic_tls()
    print()
    print("===PERCENTAGE IMPROVEMENT===",)
    print("Total Number of Vehicles Crossed",round((a2-a1)/a1*100,2),"%")
    print("Average Waiting Time",round((b1-b2)/b1*100,2),"%")
    # print("Total CO2 Emission",round((c1-c2)/c1*100,2),"%")
    # print("Total Fuel Consumption",round((d1-d2)/d1*100,2),"%")
    print()


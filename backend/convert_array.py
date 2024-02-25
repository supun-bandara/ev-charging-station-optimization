import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

def convert_array(self, current_time, array):
    for sub_array in array:
        charger_id = sub_array[0]
        current_soc = sub_array[1]
        end_soc = sub_array[2]
        arrival_time=sub_array[3]
        departure_time = sub_array[4]
        battery_capacity = sub_array[5]
        charging_power = sub_array[6]
        charging_price = sub_array[7]
        if end_soc !=0:    
            self.chargers[charger_id] = 1
            self.res_parking_time[charger_id] = time_diff(departure_time,current_time)
            self.res_charging_demand[charger_id] = battery_capacity * (end_soc - current_soc) / 100
            self.battery_capacity[charger_id] = battery_capacity
            self.current_soc[charger_id] = current_soc
            self.end_soc[charger_id] = end_soc
            self.arrival_time[charger_id] = arrival_time
            self.departure_time[charger_id] = departure_time
            self.charging_price[charger_id] = charging_price
            self.charging_power[charger_id] = charging_power
    return

def time_diff(t1,t2):
        if t1==0 or  t2==0 :     
            return 0
        elif t1==str(0) or  t2==str(0) :     
            return 0
        elif t1=='00:00' or  t2=='00:00' :     
            return 0
        else:
            print(t1)
            print(t2)
            t1_split = t1.split(":")
            t2_split = t2.split(":")
            # t1_split_hour_and_minutes
            hour = int(t1_split[0])
            minute = int(t1_split[1])
            time1_min =hour*60+minute
            print("time1",time1_min)
            
            # t2_split_hour_and_minutes
            hour = int(t2_split[0])
            minute = int(t2_split[1])
            time2_min =hour*60+minute
            print("time2",time2_min)
            
            _15_min_slots=int((time2_min-time1_min)/15)
                
            print("15 min slots",_15_min_slots)
            return _15_min_slots 
# [charger id, current soc, required soc, arrival time, departure time, battery capacity]

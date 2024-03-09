###################################################
#pandapower

import pandapower.plotting as plot
from pandapower.networks import mv_oberrhein
import pandapower as pp
import random
###mv_oberhein  20 kV network serviced by two 25 MVA HV/MV transformer stations
##141 MV/LV substations and 6 MV loads through four MV feeders

plot.plotly.mapbox_plot.set_mapbox_token('pk.eyJ1IjoiamF5YXNoYW4iLCJhIjoiY2xxbTVlcHBnMnkyMjJsbzQyaWhkcm55ciJ9.NqC5gmPq2oQYGhR7jkISjQ')

class Pandapower():
    def __init__(self,current_time):
        self.net,_= mv_oberrhein(separation_by_sub=True)
        self.min_voltage_drop_=0.98
        
        self.initialize_network()   
        self.create_load_charge_S(78 ,0,0)  #load initialize charging station
        self.uniform_loads=0.2055
            
        #self.random_loads()
        #charging station
        
         #charging station bus
        #self.uniform_load()      # if we wanna run a uniform loads

        # self.maximum_power(78)
        # self.charging_station_power(78 ,self.station_power,0)
        # self.open_network(self.net)
    
        # bus 48(index 78) - charging station / line 183 -line 161
        # bus 38 - highh voltage bus
        #self.maximum_power(self.net,0)
        
        # self.show_buses(self.net)   #show bus details
        # self.show_lines(self.net)   #show line details
        # self.show_transformer(self.net)   #show transfomer details
        #self.show_loads(self.net)
        #self.net.load.at[1, 'p_mw'] = 10.0
             
    def time_loads_random(self,current_time):
        if current_time<"6:00":   
            self.random_loads_value= [random.uniform(0, 0.01) for _ in range(68)]
            
        elif current_time>"6:00" & current_time< "8:00":
            self.random_loads_value= [random.uniform(0, 0.05) for _ in range(68)] 
            
        elif current_time>"6:00" & current_time< "8:00":
            self.random_loads_value= [random.uniform(0, 0.01) for _ in range(68)] 
        
    def time_loads_uniform(self,current_time):
        
        if current_time<"6:00":   
            self.uniform_loads=0.3 
        elif  current_time>"6:00":
            self.uniform_loads=0.6     
        
    def initialize_network(self):  
        #remove unwanted loads
        self.net.load.drop(index=143 , inplace=True)
        self.net.load.drop(index=144 , inplace=True)
        self.net.load.drop(index=145 , inplace=True)
        self.net.load.drop(index=146 , inplace=True)
        
        # Get a set of bus names connected to loads
        #buses_with_loads = set(self.net.load.bus.map(lambda bus_idx: self.net.bus.at[bus_idx, 'name']))       
        #all_buses = set(self.net.bus.name)
        #buses_without_loads = all_buses - buses_with_loads       
        # Print the results
        #print("Buses without loads:")
        #print(buses_without_loads)       
        #{'Bus 56', 'Bus 48', 'Bus 35', 'Bus 12', 'Bus 140', 'Bus 53', 'Bus 38', 'Bus 87', 'Bus 54', 'Bus 32', 'Bus 39', 'Bus 19', 'Bus 28'}
        
        bus_names_no_loads=["Bus 56", "Bus 35", "Bus 12", "Bus 140", "Bus 53", "Bus 87", "Bus 54", "Bus 32", "Bus 39", "Bus 19", "Bus 28"]
        
        for i in range(len(bus_names_no_loads)):
                      
            bus_no_load = bus_names_no_loads[i]
            pp.create_load(self.net, bus=self.net.bus.query(f'name == "{bus_no_load}"').index[0], p_mw=0.2, q_mvar=0.1, name=bus_no_load)
        
               
    def maximum_power(self,bus_index):
        print(self.net.res_bus.loc[bus_index, 'vm_pu'])

        while(self.net.res_bus.loc[bus_index, 'vm_pu']>self.min_voltage_drop_):
            print(self.net.res_bus.loc[bus_index, 'vm_pu'])  
            self.net.load.at[151, 'p_mw'] += 0.1
            
            self.run_calculation()  
        print("max  power_mw",self.net.load.at[151, 'p_mw'])                                             
        return  self.net.load.at[151, 'p_mw']  

    def show_loads(self,net):
        print(net.load)                  #show load details
                  
    def show_buses(self,net):            #show bus details
        print(net.bus)
        
    def show_lines(self,net):            #show line details
        print(net.line)
        
    def show_transformer(self,net):      #show transfomer details     
        print(net.trafo)
        
    def create_load_charge_S(self,bus,active_power,reactive_power):
        pp.create_load(self.net,bus, p_mw=active_power/1000, q_kvar=reactive_power, name="Charging Station")


    def create_transfomer(net,bus,hv_side_bus,lv_side_bus,hv_side_V,lv_side_V,max_loading):
        pp.create_transformer(net,bus, hv_bus=hv_side_bus, lv_bus=lv_side_bus,
                              max_loading_percent=max_loading,
                              vn_hv_kv=hv_side_V, vn_lv_kv=lv_side_V )
    def run_calculation(self):
        pp.runpp(self.net)
        
    def open_network(self):
        plot.plotly.pf_res_plotly(self.net, on_map=True, projection='epsg:31467', map_style='satellite')
    
    def uniform_load(self):                            #assigning all loads are equals
        #print("index",self.net.load.index)
        
        for i in range(len(self.net.load.index)):
            self.net.load.at[self.net.load.index[i], 'p_mw'] = self.uniform_loads   #assigning active power
            self.net.load.at[self.net.load.index[i], 'q_mvar'] = self.uniform_loads #assigning reactive power
            
    def random_loads(self):
         for i in range(len(self.net.load.index)):
            self.net.load.at[self.net.load.index[i], 'p_mw'] = self.random_loads_value[i]  #assigning active power
            self.net.load.at[self.net.load.index[i], 'q_mvar'] = self.random_loads_value[i] #assigning reactive power
    
    def limitation_element(self):
         print(pp.contingency.get_element_limits(self.net))    
            
    def charging_station_power(self,bus,active_power,reactive_power):
        self.net.load.at[151, 'p_mw'] = active_power/1000
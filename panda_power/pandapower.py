###################################################
#pandapower

import pandapower.plotting as plot
from pandapower.networks import mv_oberrhein
import pandapower as pp

###mv_oberhein  20 kV network serviced by two 25 MVA HV/MV transformer stations
##141 MV/LV substations and 6 MV loads through four MV feeders


plot.plotly.mapbox_plot.set_mapbox_token('pk.eyJ1IjoiamF5YXNoYW4iLCJhIjoiY2xxbTVlcHBnMnkyMjJsbzQyaWhkcm55ciJ9.NqC5gmPq2oQYGhR7jkISjQ')

class pandapower():
    def __init__(self):
        self.net,_= mv_oberrhein(separation_by_sub=True)

        self.create_load(self.net,100,3,2)
        self.run_calculation(self.net)
        #self.maximum_power(self.net,0)
        self.open_network(self.net)
        #self.show_buses(self.net)   #show bus details
        #self.show_lines(self.net)   #show line details
        #self.show_transformer(self.net)   #show transfomer details
        self.show_loads(self.net)
        
    def maximum_power(self,net,bus):
        pp.opf_task(net)
        max_power = net.res_bus.at[bus, 'p_kw_max']
        return max_power
    
    def show_loads(self,net):
        print(net.load)         #show load details
                  
    def show_buses(self,net):   #show bus details
        print(net.bus)
        
    def show_lines(self,net):   #show line details
        print(net.line)
        
    def show_transformer(self,net):      #show transfomer details     
        print(net.trafo)
        
    def create_load(self,net,bus,active_power,reactive_power):
        pp.create_load(net,bus, p_mw=active_power, q_kvar=reactive_power, name="Load 1")

    def create_transfomer(net,bus,hv_side_bus,lv_side_bus,hv_side_V,lv_side_V,max_loading):
        pp.create_transformer(net,bus, hv_bus=hv_side_bus, lv_bus=lv_side_bus,
                              max_loading_percent=max_loading,
                              vn_hv_kv=hv_side_V, vn_lv_kv=lv_side_V )
    def run_calculation(self,net):
        pp.runpp(net)
        
    def open_network(self,net):
        plot.plotly.pf_res_plotly(net, on_map=True, projection='epsg:31467', map_style='satellite')
    
    #def uniform_load():
    #    pp.create_load(net,bus, p_mw=active_power, q_kvar=reactive_power, name="Load 1")
    
    
pandapower()
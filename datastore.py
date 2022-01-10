'''
Created on 3 May 2017

@author: jackw
@amended by Brian F

Naming convention
- Variables = no spaces, capitals for every word except the first : thisIsAVariable
- Local functions = prefixed with _, _ for spaces, no capitals : _a_local_function

Dependencies
-NI VISA Backend
-Non standard python modules
    pyvisa
    pyserial


to do:
-complete button on TPW doesn't work
-TPW freezes if a probe is inserted
-add SQ probe to list

#         s = ttk.Separator(self.root, orient=VERTICAL)
#         s.grid(row=0, column=1, sticky=(N,S))

'''


import pickle
import os




class DataStore():
  
   
        
        ########################
        # Main data file read  #
        ########################
    def get_user(self):
        with open('file.user', 'rb') as load_user_file:
            load_data = pickle.load(load_user_file)
        load_user_file.close()
       
        return load_data
        ###########################
        # Batch control file read #
        ###########################
    def get_batch(self):
        with open("file.batch", "rb") as load_batch_file:
            temp_load = pickle.load(load_batch_file)
        load_batch_file.close()
        return temp_load
    
        ###########################
        # Admin control file read #
        ###########################
    def get_admin(self):
        with open('file.admin', 'rb') as load_admin_file:
            admin_load = pickle.load(load_admin_file)
        load_admin_file.close()
        return admin_load
    
    #######################################
    
    def get_ports(self):
        with open('file.ports', 'rb') as load_ports_file:
            port_load = pickle.load(load_ports_file)
        load_ports_file.close()
        return port_load
    
    #######################################
    
    def get_keyboard_data(self):
        with open('file.keys','rb') as load_keys:
            keys_data = pickle.load(load_keys)
        load_keys.close()
     
        return keys_data
    
    #########################################
        
    def write_to_user_file(self, user_data):
        with open('file.user', 'wb') as user_file:
            pickle.dump(user_data, user_file)
        user_file.close()
        
    ########################################
    
    def write_to_batch_file(self, batch_data):
        with open('file.batch', 'wb') as batch_file:
            pickle.dump(batch_data, batch_file)
        batch_file.close()
    
    #########################################
    
    def write_to_admin_file(self, admin_data):
        with open('file.admin', 'wb') as file:
            pickle.dump(admin_data, file)
        file.close()
        
    #########################################
    
    def write_to_port_file(self, ports):
        with open('file.ports', 'wb') as port_file:
            pickle.dump(ports, port_file)
        port_file.close()
        
    ##########################################
    
    def write_to_from_keys(self, keys):
        with open('file.keys', 'wb') as key_input:
            pickle.dump(keys, key_input)
        key_input.close()
    
    ##########################################   
    
    def write_file_location(self, location):
        with open('location', 'wb') as file:
            pickle.dump(location, file)
        file.close()

    ##########################################

    def add_to_user_file(self, user_data):
        user_load = []
        user_load.extend( self.get_user())
        user_load.append(user_data)
        self.write_to_user_file(user_load)
    
    #########################################
    
    def add_to_batch_file(self, batch_data):
        load_data = []
        load_data.extend(self.get_batch())
        load_data.append(batch_data)
        self.write_to_batch_file(load_data)
        
    #########################################
    
    def add_to_admin_file(self, admin_data):
        temp_load = []
        temp_load.append(self.get_admin())
        temp_load.append(admin_data)
        self.write_to_admin_file(temp_load)
        
    #########################################
    
    def get_user_admin_status(self):
        admin = []
        admin.extend(self.get_user())
        return admin[1]
    
    #########################################
    
    def get_username(self):
        return self.get_user()[0]
    
    #########################################
        
    
    def get_programme_status(self):
        ok = []
        ok.extend(self.get_admin())
        if "1" in ok:
            return True
        else:
            return False
        
    ########################################
    
    def get_user_status(self):
        if "1" in self.get_admin():
            return True
        else:
            return False
        
    #########################################
    
    def show_all_data(self):
            print(f"all data = main {self.get_user()}, batch {self.get_batch()}, admin {self.get_admin()}")
            print(f"Probe port {self.get_probe_port()}, Analyser port {self.get_analyser_port()}")
            print(f"ODM port {self.get_ODM_port()} , file location {self.get_location_file()}")

     #########################################

    def get_analyser_port(self):
        return self.get_ports()[1]

    ###########################################

    def set_analyser_port(self, port):
        ports = self.get_ports()
        ports[1] = port
        self.write_to_port_file(ports)
        
    ###########################################

    def get_ODM_port(self):
        odm_port = ""
        odm_port = self.get_ports()
        return odm_port[2]

    ###########################################

    def set_ODM_port(self, port):
        ports = self.get_ports()
        ports[2] = port
        self.write_to_port_file(ports)
        
    ###########################################

    def set_probe_port_obj(self, obj):
        ports = self.get_ports()
        ports[3] = obj
        self.write_to_port_file(ports)

    ###########################################

    def get_probe_port_obj(self):
        return self.get_ports()[3]

    ###########################################    

    def get_probe_port(self):
        return self.get_ports()[0]

    ############################################

    def set_porbe_port(self, port):
        ports = self.get_ports()
        ports[0] = port
        self.write_to_port_file(ports)
       
    ############################################

    def get_current_batch(self):
        return self.get_batch()[0]

    ############################################

    def get_current_probe_type(self):
        return self.get_batch()[1]
        
    ############################################
    
    def get_plot_status(self):
        user_plot = self.get_user()
        return user_plot[2]
    
    ############################################
    
    def set_plot_status(self, plot):
        user_status = []
        user_status.extend(self.get_user())
        status_len = len(user_status)
        if status_len == 3:
            user_status.pop(2)
            user_status.insert(2,plot)
        else:
            user_status.append(plot)
        self.write_to_user_file(user_status)
        
    ############################################

    def get_location_file(self):
        path1 = os.path.join("C:\\Users", os.getenv('username'),"python-dev\PTT\location")
        path2 = os.path.exists(path1)
        if path2:
            with open('location', 'rb') as load_file:
                load = pickle.load(load_file)
            load_file.close()
        else: load = False
        return load

        

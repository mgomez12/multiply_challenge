from telnetlib import Telnet
import csv

class TCSBot():

    
    def __init__(self, sim=None, ip='192.168.0.1', default_cartesian=True):
        
        self.sim = sim
        if not sim:
            self.tn = Telnet(ip)
        resp = self.attach()
        if (resp[0] != 0):
            raise Exception("Unable to attach")
        self.default_cartesian = default_cartesian
        
        
    def send_cmd(self, s):
        if self.sim:
            self.sim.write(s)
        else:
            tn.write(s.encode('ascii') + b"\n")
        return self.get_resp()
    def get_resp(self):
        if self.sim:
            return [int(i) for i in (self.sim.resp().split(' '))]
        else:
            return [int(i) for i in tn.read_until('\n').decode('ascii').split(' ')]

    
    def read_from_csv(self, fname, cartesian=None):
        if (cartesian == None):
            cartesian = self.default_cartesian
        with open(fname, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                resp = self.send_loc(row[0], tuple(row[1:]), cartesian)
                if (resp[0] != 0):
                    return resp
                
        
    def attach(self):
        return self.send_cmd("attach 1")
    def release(self):
        return self.send_cmd("attach 0")
    def shutdown(self):
        self.release() # add error checking
        return self.send_cmd("exit")
        
    def send_loc(self, ix, position, cartesian=None):
        cmd = ' '.join([str(i) for i in position])
        if (cartesian == None):
            cartesian = self.default_cartesian
        if (cartesian):
            return self.send_cmd(f'locXyz {ix} ' + cmd)
        else:
            return self.send_cmd(f'locAngles {ix} '  + cmd)
        
    def station_move(self, ix, profile):
        return self.send_cmd(f'Move {ix} {profile}')
    
    def get_curr_loc(self, cartesian=None):
        if (cartesian == None):
            cartesian = self.default_cartesian
        if cartesian:
            return self.send_cmd("wherec")
        else:
            return self.send_cmd("wherej")

    def get_goal_loc(self, cartesian=None):
        if (cartesian == None):
            cartesian = self.default_cartesian
        if cartesian:
            return self.send_cmd("DestC")
        else:
            return self.send_cmd("DestJ")


    #note: might not be future proof if default values get updated in robot since
    # they would also have to be changed here
    def teach_plate(self, ix, z_clearance=50):
        return self.send_cmd(f'TeachPlate {ix} {z_clearance}')
    def pick_plate(self, ix, horiz_comp=0, comp_torque=0):
        return self.send_cmd(f'PickPlate {ix} {horiz_comp} {comp_torque}')
    def place_plate(self, ix, horiz_comp=0, comp_torque=0):
        return self.send_cmd(f'PlacePlate {ix} {horiz_comp} {comp_torque}')
    def move_plate(self, from_ix, to_ix, horiz_comp=0, comp_torque=0):
        first_resp = self.pick_plate(from_ix, horiz_comp, comp_torque)
        if first_resp[0] != 0:
            return first_resp
        else:
            return self.place_plate(to_ix, horiz_comp, comp_torque)
        

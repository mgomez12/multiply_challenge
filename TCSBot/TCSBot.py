from telnetlib import Telnet
import csv


class RobotError:
    """
    Special class for robot errors, in order to distinguish robot error output from
    """
    def __init__(self, resp, attempted_command):
        self.resp = tuple(resp)
        self.cmd = attempted_command
        
    def __repr__(self):
        return "RobotError: Command " + self.cmd + ", Response: " + " ".join(self.resp)

    def get_error_output(self):
        return self.resp
    def get_faulty_command(self):
        return self.cmd





class TCSBot:
    """
    Main TCSBot class, uses TCS commands to communicate

    """

    
    def __init__(self, sim=None, ip='192.168.0.1', default_cartesian=True):
        """
        Creates new instance of bot driver and connects to either Telnet or a
        simulated server (sim must have write(s) and resp() commands). 

            Parameters:
                sim(optional): a class with write and response commands to simulate
                               Telnet activity
                ip(optional): IP address of robot arm
                default_cartesian(optional): set either cartesian or angle system
        """
        
        self.sim = sim
        if not sim:
            self.tn = Telnet(ip)
        resp = self.attach()
        if (resp != 0):
            print(resp)
            raise Exception("Unable to attach")
        self.default_cartesian = default_cartesian
        
        
    def send_cmd(self, s):
        """
        Sends a command to the robot and returns the response

            Parameters:
                s: string to send
            Returns: list of returned strings from robot if successful, or RobotError instance otherwise
        """
        
        if self.sim:
            self.sim.write(s)
        else:
            tn.write(s.encode('ascii') + b"\n")
        resp = self.get_resp()
        if resp[0] == '0':
            return resp
        return RobotError(resp, s)
    
    def get_resp(self):
        """
        Obtains response from robot

            Returns: list of returned strings from robot
        """
        
        if self.sim:
            return self.sim.resp().split(' ')
        else:
            return tn.read_until('\n').decode('ascii').split(' ')

    
    def read_from_csv(self, fname, cartesian=None):
        """
        Loads positions from csv file. Each row must be formatted as follows:
            ix, coord1, coord2, coord3, etc
            ix, coord1, coord2, coord3, etc

            Returns: 0 if successful, or RobotError instance if not
        """
        
        if (cartesian == None):
            cartesian = self.default_cartesian
        with open(fname, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                resp = self.set_station(row[0], tuple(row[1:]), cartesian)
                if (resp != 0):
                    return resp
        return 0
                
        
    def attach(self):
        """
        Releases robot

            Returns: 0 if successful, or RobotError instance if not
        """
        
        resp = self.send_cmd("attach 1")
        if type(resp) == RobotError:
            return resp
        else:
            return 0
    
    def release(self):
        """
        Releases robot

            Returns: 0 if successful, or RobotError instance if not
        """
        
        resp = self.send_cmd("attach 0")
        if type(resp) == RobotError:
            return resp
        else:
            return 0
    
    def shutdown(self):
        """
        Releases robot and closes communication channel

            Returns: 0 if successful, or RobotError instance if not
        """
        
        resp = self.release()
        if (resp != 0):
            return resp
        resp = self.send_cmd("exit")
        if type(resp) == RobotError:
            return resp
        else:
            return 0
        
    def set_station(self, ix, position, cartesian=None):
        """
        Sets a station to a position that is passed in.

            Parameters:
                ix: station index to use
                position: a tuple containing the position coordinates
                cartesian(optional): boolean stating if working with cartesian, defaults
                                     to value defined in constructor if not included
            Returns: 0 if successful, or RobotError instance if not
        """
        
        cmd = ' '.join([str(i) for i in position])
        if (cartesian == None):
            cartesian = self.default_cartesian
        if (cartesian):
            resp = self.send_cmd(f'locXyz {ix} ' + cmd)
        else:
            resp = self.send_cmd(f'locAngles {ix} '  + cmd)
        if type(resp) == RobotError:
            return resp
        else:
            return 0
        
    def station_move(self, ix, profile):
        """
        Moves robot to a station

            Parameters:
                ix: station index to use
                profile: profile index to use
            Returns: 0 if successful, or RobotError instance if not
        """
        resp = self.send_cmd(f'Move {ix} {profile}')
        if type(resp) == RobotError:
            return resp
        else:
            return 0

    
    def get_curr_loc(self, cartesian=None):
        """
        Obtains current location

            Parameters:
                cartesian(optional): boolean stating if working with cartesian, defaults
                                     to value defined in constructor if not included
            Returns: current position tuple if successful, or RobotError instance if not
        """
        if (cartesian == None):
            cartesian = self.default_cartesian
        if cartesian:
            resp = self.send_cmd("wherec")
        else:
            resp = self.send_cmd("wherej")

        if type(resp) == RobotError:
            return resp
        else:
            return tuple([int(i) for i in resp[1:]])


    def get_goal_loc(self, cartesian=None):
        """
        Obtains goal location

            Parameters:
                cartesian(optional): boolean stating if working with cartesian, defaults
                                     to value defined in constructor if not included
            Returns: goal position tuple if successful, or RobotError instance if not
        """
        
        if (cartesian == None):
            cartesian = self.default_cartesian
        if cartesian:
            resp = self.send_cmd("DestC")
        else:
            resp = self.send_cmd("DestJ")

        if type(resp) == RobotError:
            return resp
        else:
            return tuple([int(i) for i in resp[1:]])


    #note: might not be future proof if default values get updated in robot since
    # they would also have to be changed here
    def teach_plate(self, ix, z_clearance=50):
        """
        Teaches robot plate location

            Parameters:
                ix: staton index to use
                z_clearance(optional): Z clearance to use, defaults to robot default of 50
            Returns: 0 if successful, or RobotError instance if not
        """
        
        resp = self.send_cmd(f'TeachPlate {ix} {z_clearance}')
        if type(resp) == RobotError:
            return resp
        else:
            return 0

        
    def pick_plate(self, ix, horiz_comp=False, comp_torque=0):
        """
        Pick up plate from location

            Parameters:
                ix: staton index to use
                horiz_comp: True if should enable horizontal compliance
                comp_torque: sets % of original horizontal holding torque to be retained during compliance
            Returns: 0 if successful, or RobotError instance if not
        """
        
        resp = self.send_cmd(f'PickPlate {ix} {int(horiz_comp)} {comp_torque}')
        if type(resp) == RobotError:
            return resp
        else:
            return 0

        
    def place_plate(self, ix, horiz_comp=False, comp_torque=0):
        """
        Place plate at location

            Parameters:
                ix: staton index to use
                horiz_comp: True if should enable horizontal compliance
                comp_torque: sets % of original horizontal holding torque to be retained during compliance
            Returns: 0 if successful, or RobotError instance if not
        """
        
        resp = self.send_cmd(f'PlacePlate {ix} {int(horiz_comp)} {comp_torque}')
        if type(resp) == RobotError:
            return resp
        else:
            return 0

        
    def move_plate(self, from_ix, to_ix, horiz_comp=False, comp_torque=0):
        """
        Pick up plate from one location and set it down at another

            Parameters:
                ix: staton index to use
                horiz_comp: True if should enable horizontal compliance
                comp_torque: sets % of original horizontal holding torque to be retained during compliance
            Returns: 0 if successful, or RobotError instance if not
        """
        
        first_resp = self.pick_plate(from_ix, horiz_comp, comp_torque)
        if first_resp != 0:
            return first_resp
        else:
            resp = self.place_plate(to_ix, horiz_comp, comp_torque)
        if type(resp) == RobotError:
            return resp
        else:
            return 0
        

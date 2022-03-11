from TCSBot import TCSBot


class Sim:
    """
    Dummy response simulator to test input and output handling. This is NOT
    ACTUALLY FUNCTIONAL, AND CERTAIN VALID COMMANDS RETURN ERRORS in order to
    test the driver's error handling mechanisms

    """
    def __init__(self):
        self.is_cart = {}
        self.locs = {}
        self.profiles = {1:{'speed':0}}
        self.curr_loc = (0,0,0, 1, 4, 3)
        self.dest_loc = (2,4,2,4,5,7)
        self.resp_buf = []
        self.attached = False
        pass

    def write(self, s):
        args = s.split()
        print(s)
        if (args[0] == "attach"):
            if args[1] == 1: 
                self.attached = True
                self.resp_buf = [0]
            else:
                self.attached = False
                self.resp_buf = [0]
        elif (args[0] == "locXyz"):
            if args[0] in self.is_cart and self.is_cart[args[0]] and len(args)==1:
                self.resp_buf = [-1]
            else:
                self.is_cart[args[0]] = True
                self.locs[args[1]] = tuple(args[2:])
                self.resp_buf = [0, args[1]]
        elif (args[0] == "wherec"):
            self.resp_buf = [0] + [i for i in self.curr_loc]
            
        elif (args[0] == "DestJ"):
            self.resp_buf = [0] + [i for i in self.dest_loc]
        else:
            self.resp_buf = [-1]
                
        
    def resp(self):
        return ' '.join([str(i) for i in self.resp_buf])




#---------------------------------------------------------------#

    
s = Sim()
b = TCSBot(s)

print(b.set_station(0,(1,2,3,1,2,3)))
print()
print(b.get_curr_loc())
print()
print(b.set_station(1, (4, 8, 4), cartesian=False))
print()
print(b.get_goal_loc(cartesian=False))
print()
print(b.teach_plate(2))
print()
print(b.pick_plate(2))
print()
print(b.place_plate(2,1,30))
print()
print(b.move_plate(2, 5, 1))
print()
print(b.read_from_csv('dummy_locs.csv'))
print()
print(b.read_from_csv('dummy_locs.csv', cartesian=False))

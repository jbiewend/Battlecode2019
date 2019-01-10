from battlecode import BCAbstractRobot, SPECS
import battlecode as bc

# import random

__pragma__('iconv')
__pragma__('tconv')
# __pragma__('opov')


class MyRobot(BCAbstractRobot):
    step = -1

    def __init__(self):
        # We can encode the 16-bit signal to have as much information as we want
        # B - # of bad guys in the area
        # K - # of Karbonite the unit can see
        # F - # of Fuel the unit can see
        # C - First two bits are karbonite, second two bits are fuel
        # BBBB KKKK FFFF CCCC
        # 0000 0000 0000 0000
        self.radio_list = ['baddie_in_sight', 'karbonite_in_sight', 'fuel_in_sight', 'karbonite_held', 'fuel_held']
        self.radio_shift_amt_list = [12, 8, 4, 2, 0]
        self.radio_mask_list = [0xf000, 0x0f00, 0x00f0, 0x000c, 0x0003]

        BCAbstractRobot.__init__(self)
        self.radio_data = {}
        # These are the max values so they are the default values (and should be ignored)
        self.radio_data['baddie_in_sight'] = 0xf
        self.radio_data['karbonite_in_sight'] = 0xf
        self.radio_data['fuel_in_sight'] = 0xf
        self.radio_data['karbonite_held'] = 0x3
        self.radio_data['fuel_held'] = 0x3

        self.log("A new unit is born!")

        # TODO save the spawning castle's location for resource dump

    def turn(self):
        self.encode_radio_message()
        self.step += 1
        self.log("START TURN " + self.step)

        if self.me['unit'] == SPECS['CASTLE']:
            self.log("I am a castle.")
            if self.step % 10 == 0:
                self.log("Global Karbonite Level: " + self.karbonite)
                self.log("Global Fuel Level: " + self.fuel)
                # TODO change the below line to build anywhere it can, not just up and right one square
                return self.build_unit(SPECS['PILGRIM'], 1, 1)

            else:
                self.log("Castle health: " + self.me['health'])

        elif self.me['unit'] == SPECS['CHURCH']:
            self.log("I am a church.")

        elif self.me['unit'] == SPECS['PILGRIM']:
            self.log("I am a pilgrim.")
            self.log("Karbonite Level: " + self.me.karbonite)
            self.log("Fuel Level: " + self.me.fuel)
            am_i_on_karbonite = self.on_karbonite(self.me.x, self.me.y)
            am_i_on_fuel = self.on_fuel(self.me.x, self.me.y)

            if self.me.fuel > 90 or self.me.karbonite > 18:
                # return to castle
                self.log("I need to drop off resources but I'm lost")
            elif am_i_on_karbonite or am_i_on_fuel:
                self.log("I am on a resource.")
                return self.mine()
            else:
                # wander aimlessly (by aimlessly we mean in a predetermined direction)
                self.log("I'm trying to move.")
                return move_randomly_single()

        elif self.me['unit'] == SPECS['CRUSADER']:
            self.log("I am a nighthawk.")
            self.log("Crusader health: " + str(self.me['health']))
            # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
            choices = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
            # choice = random.choice(choices)
            choice = choices[0]
            self.log('TRYING TO MOVE IN DIRECTION ' + str(choice))
            return self.move(*choice)

        elif self.me['unit'] == SPECS['PROPHET']:
            self.log("I am a prophet.")

        elif self.me['unit'] == SPECS['PREACHER']:
            self.log("I am a preacher.")


# private helper methods
    def move_randomly_single(self):
        # TODO Make this actually move randomly!!
        # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
        choices = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        # choice = random.choice(choices)
        choice = choices[0]
        self.log('TRYING TO MOVE IN DIRECTION ' + str(choice))
        return self.move(*choice)

    def move_fast(self):
        # Jump to the farthest possible range, then work back toward one square.
        pass

    def build_randomly(self):
        pass

    def on_karbonite(self, x, y):
        map = self.karbonite_map
        on_resource = map[y][x]
        this.log("on karbonite:" + on_resource)
        return on_resource

    def on_fuel(self, x, y):
        map = self.fuel_map
        on_resource = map[y][x]
        this.log("on fuel:" + on_resource)
        return on_resource

    def encode_radio_message(self):
        final_msg = 0
        for idx, msg in enumerate(self.radio_list):
            final_msg += self.radio_data[msg] << self.radio_shift_amt_list[idx]
        self.log("Encoded message: {}".format(final_msg))
        self.log("Decoded message: {}".format(self.decode_radio_message(final_msg)))
        return final_msg

    def decode_radio_message(self, message):
        data_output = {}
        for idx, msg_name in enumerate(self.radio_list):
            msg_value = message & self.radio_mask_list[idx]
            msg_value = msg_value >> self.radio_shift_amt_list[idx]
            data_output[msg_name] = msg_value

        return data_output


robot = MyRobot()

# from battlecode import BCAbstractRobot, SPECS
# import battlecode as bc
# import random
#
# __pragma__('iconv')
# __pragma__('tconv')
# __pragma__('opov')
#
# # don't try to use global variables!!
# class MyRobot(BCAbstractRobot):
#     step = -1
#
#     def turn(self):
#         self.step += 1
#         self.log("START TURN " + self.step)
#         if self.me['unit'] == SPECS['CRUSADER']:
#             self.log("Crusader health: " + str(self.me['health']))
#
#             visible = self.get_visible_robots()
#
#             # get attackable robots
#             attackable = []
#             for r in visible:
#                 # x = 5
#                 # if not self.is_visible(r):
#                 if 'x' not in r: #not visible. hacky. do not use at home
#                     continue
#                 # now all in vision range, can see x, y etc
#                 dist = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2
#                 if r['team'] != self.me['team'] and SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][0] <= dist and SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][1] >= dist:
#                     attackable.append(r)
#
#             if attackable:
#                 # attack first robot
#                 r = attackable[1]
#                 self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
#                 return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])
#
#             # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
#             choices = [(0,-1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
#             choice = random.choice(choices)
#             self.log('TRYING TO MOVE IN DIRECTION ' + str(choice))
#             return self.move(*choice)
#
#         elif self.me['unit'] == SPECS['CASTLE']:
#             if self.step < 10:
#                 self.log("Building a crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
#                 return self.build_unit(SPECS['CRUSADER'], 1, 1)
#
#             else:
#                 self.log("Castle health: " + self.me['health'])
#
# robot = MyRobot()
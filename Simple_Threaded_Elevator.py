import time
import threading

DEBUG_ON = False

# Building setup
TOP_FLOOR = 10
BOTTOM_FLOOR = 1
NUM_FLOORS = TOP_FLOOR - BOTTOM_FLOOR + 1

# Elevator car travel direction
ST = "stopped"
UP = "moving_up"
DN = "moving_dn"

# Wait time
CAR_MOVEMENT_TIME_BETWEEN_FLOORS = 2
DOOR_WAIT = 5

# Class to store, share, and manipulate the elevator button column as '0's and '1's.
class shareddata:
    
    def __init__(self):
        self.buttons = [0 for i in range(NUM_FLOORS)] 
        self.direction = ST
        self.curr_floor = BOTTOM_FLOOR

    def lowest_button_on(self): 
        for i, x in enumerate(self.buttons):
            
            if x == 1:
                return int(i+1)
      
    def highest_button_on(self):
        j = 0
        for i, x in enumerate(reversed(self.buttons)):
            
            if x == 1:
                return int(NUM_FLOORS-i)
     
    def any_button_pressed(self):
        for i, x in enumerate (self.buttons):
            if x == 1:
                return True
        return False
        
    def clear_button(self, i):
        self.buttons[i] = 0
        return

    def set_button(self, i):
        self.buttons[i] = 1
        return
        
    
# instantiate sharedData object
sharedData = shareddata() 

## Begin Elevator car thread
def elevator_car():
    while True:    
        # Print current floor
        print("elevator_car(): curr_floor=", sharedData.curr_floor);
        print("elevator_car(): Direction: ", sharedData.direction)
        if (DEBUG_ON):
            print("*** elevator_car(): Buttons: ", sharedData.buttons)
            print("*** elevator_car(): Lowest button: ", sharedData.lowest_button_on())
            print("*** elevator_car(): Highest button: ", sharedData.highest_button_on())
            print("*** elevator_car(): Any button pressed: ", sharedData.any_button_pressed())
            
      
        # Arrived on a floor whose button was pushed
            
        if sharedData.any_button_pressed() and (sharedData.direction == UP or sharedData.direction == DN) and sharedData.buttons[sharedData.curr_floor-1] == 1:
            # Unlight/clear button
            sharedData.clear_button(sharedData.curr_floor-1)
           
            print("elevator_car(): Open door on floor: ", sharedData.curr_floor)
            time.sleep(DOOR_WAIT)
            print ("elecator_car(): Close door on floor:", sharedData.curr_floor)
          
        # Logic for no overruns. This is the situation when elevator 
        # gets to the highest floor it was directed to, moving up, 
        # and there are no more floors above called, but
        # there are lower floors we need to go. This means changing direction of travel from up to down. 
       
        if sharedData.any_button_pressed() and sharedData.highest_button_on() < sharedData.curr_floor:
            sharedData.direction = DN

        # Similarly, when going down, once stopped on the lowest floor, and there
        # is an higher floor pushed, change direction to up.

        if sharedData.any_button_pressed() and sharedData.lowest_button_on() > sharedData.curr_floor:
            sharedData.direction = UP


        # Move elevator car
        if sharedData.direction == UP and sharedData.any_button_pressed():
            sharedData.curr_floor = sharedData.curr_floor + 1 
        if sharedData.direction == DN and sharedData.any_button_pressed():
            sharedData.curr_floor = sharedData.curr_floor - 1
        
        time.sleep(CAR_MOVEMENT_TIME_BETWEEN_FLOORS)
## End Elevator car thread

## Begin buttons read thread
def elevator_buttons():
    while True:
        f = input("Input floor number:\n")
        try:
            f = int (f)
        except:
            print("input invalid")
        if isinstance(f, int) and f >= BOTTOM_FLOOR and f <= TOP_FLOOR:
          
            # Light/set button on button column
            sharedData.set_button(f-1)
            print("elevator_buttons(): button pushed for target floor=", f)
            
            if (DEBUG_ON):
                print("*** elevator_buttons(): sharedData.highest_button_on()", sharedData.highest_button_on())
            
## End buttons read thread

## Begin controller thread
def controller():
    while True:
        # If elevator is currently below the lowest floor pressed, then start traveling up.
        if sharedData.any_button_pressed() and sharedData.direction == ST and sharedData.lowest_button_on() > sharedData.curr_floor:
            sharedData.direction = UP
            
        # If elevator is currently above the highest floor pressed, then start traveling down.
        if sharedData.any_button_pressed() and sharedData.direction == ST and sharedData.highest_button_on() < sharedData.curr_floor:
            sharedData.direction = DN

        # If no button is pressed then stop the elevator.
        if sharedData.any_button_pressed()==False:
            sharedData.direction = ST
               
       
## End controller thread


# Launch threads from main program
if __name__ == "__main__":

    # creating threads
    e1 = threading.Thread(target=elevator_car, name="e1")
    b1 = threading.Thread(target=elevator_buttons, name="b1")
    c1 = threading.Thread(target=controller, name="c1")

    # starting threads
    e1.start()
    b1.start()
    c1.start()

    # wait until all threads finish
    e1.join()
    b1.join()
    c1.join()
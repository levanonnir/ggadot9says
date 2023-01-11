import nxt.locator,nxt.motor,nxt.sensor,time
from globals import COLORS
# moving:
# run(power)  #run at 'power' speed, [-100,100], - is backwards
# time.sleep(time4Line)    #"sleep" for 'time4Line', before moving on to next command
# brake()  #stop running
# turn(power,dis2Turn)   #run at 'power' speed, only 'dis2Turn' turns of the wheels

# sensors:
# sensor_name.get_sample()    # get sensor sample
# brick.play_tone_and_wait(frequency, duration)    # play music

class Lego:
    '''
    Class to operate the Robolego nxt.
    '''
    def connect(self,name):
        '''
        Method to initialize the lego controller, left and right engine,
        light and toch sensor.
        :param name: The robolego name.
        :return: Nothing, but prints connected on screen.
        '''
        self.brick=nxt.locator.find_one_brick(name=name)

        self.left=nxt.motor.Motor(self.brick,nxt.motor.PORT_A)
        self.right=nxt.motor.Motor(self.brick,nxt.motor.PORT_C)
        self.touch=nxt.sensor.Touch(self.brick,nxt.sensor.PORT_2)
        self.light=nxt.sensor.Light(self.brick,nxt.sensor.PORT_3)
        self.light.set_input_mode(nxt.sensor.Type.LIGHT_ACTIVE, nxt.sensor.Mode.RAW)
        self.colors = COLORS
        self.movementDirections = [
            "forward",
            "backward",
            "turn_left",
            "turn_right",
        ]

        print('%s connected successfully.' % name)

    def forward(self, power):
        self.stop()
        # Run the left engine forward
        self.left.run(power)
        # Run the right engine forward
        self.right.run(power)

    def backward(self, power):
        self.stop()
        # Run the left engine backward
        self.left.run(-power)
        # Run the right engine backward
        self.right.run(-power)

    def turn_left(self, power):
        self.stop()
        # Run the left engine forward
        self.left.run(-1*power)
        # Run the right engine forward
        self.right.run(power)

    def turn_right(self, power):
        self.stop()
        # Run the left engine forward
        self.left.run(power)
        # Run the right engine forward
        self.right.run(-1*power)

    def stop(self):
        # Brake the left engine
        self.left.brake()
        # Brake the right engine
        self.right.brake()

    def sample_color(self):
        # Find the color number using nxt.sensor.Color20 and Get color name using colors dictionary
        color = self.colors.get(nxt.sensor.Color20(self.brick, nxt.sensor.PORT_1).get_sample())
        return color

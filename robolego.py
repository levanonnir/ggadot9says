import nxt.locator,nxt.motor,nxt.sensor,time

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

        print('Connected')

    def forward(self, power):
        self.stop()
        # Run the left engine forward
        self.left.run(power)
        # Run the right engine forward
        self.right.run(power)

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

    def cross_road(self, power, saf):
        '''
        fill the blank lines for task # 4
        :param power: Lego motor strength.
        :param saf: Threshold for determinate black or white
        :return:
        '''
        count = 0
        #Run the left engine forward
        self.left.run(power)
        #Run the right engine forward
        self.right.run(power)
        #Infinite loop
        while 1:
        #While not the touch sensor was pressed
            while not(self.touch.get_sample()):
                #while white (the white value should be above threshold).
                while self.light.get_sample() > saf :
                    print('w')
                    #If the touch sensor was pressed
                    if self.touch.get_sample():
                        break
                    #Sleeping to protect the brick
                    time.sleep(0.05)
                else:
                    # Black
                    print('b')
                    #Sleeping to protect the brick
                    time.sleep(0.05)
                    pass
                # raise counter by one
                count +=1
            print('There are %s lines in cross road' % count)
            #Brake the left engine
            self.left.brake()
            # Brake the right engine
            self.right.brake()
            #break the loop
            break

    def line_and_turn(self,power,time4Line,dis2Turn):
        '''

        :param self:
        :param power: Lego motor strength.
        :param time4Line: Sleeping time while lego drive forward,
                            determine the length of line
        :param dis2Turn: Distance to turn, determine raduis of orbit.
        :return:
        '''
        # Helper function
        self.left.run(power)
        self.right.run(power)
        time.sleep(time4Line)
        self.right.brake()
        self.left.brake()
        self.left.turn(power, dis2Turn)
        self.right.turn(-power, dis2Turn)

    def ribua(self,power,time4Line,dis2Turn):
        '''
        complete the blank lines for task 1
        :param self:
        :param power:
        :param time4Line:
        :param dis2Turn:
        :return:
        '''
        #Loop 4 times
        for i in range(4):
            #Call the helper function
            self.line_and_turn(self, power, time4Line, dis2Turn)


    def spirala(self,power, timestraight, dis2Turn, numOfSides):
        '''
        complete blank lines task-2
        :param self:
        :param power:
        :param timestraight:
        :param dis2Turn:
        :param numOfSides: Number of  edges of spiral
        :return:
        '''
        #Loop num of edges
        for i in range(numOfSides):
            #Make a spiral hint(change the parameter timestraight)
            self.line_and_turn(self, power, i*timestraight, dis2Turn)
            # __________________________


    def sing_drive(self,power):
        '''
        Fill blank lines task # 5
        Lego will drive back and forth while playing music.
        :param self:
        :param power:
        :return:
        '''
        #toggle variable value will alternate between 1 and -1 after each loop
        #this value will determine the direction of the motor.
        toggle=1
        #Infinite loop
        while 1:
            #Run the left engine forward/back
            self.left.run(power*toggle)
            #Run the right engine forward/back
            self.right.run(power*toggle)
            #play the music
            self.brick.play_tone_and_wait(262, 500)
            self.brick.play_tone_and_wait(294, 500)
            self.brick.play_tone_and_wait(330, 500)
            self.brick.play_tone_and_wait(294, 500)
            #change toggle value for the engines to turn the oppsite direction
            toggle = toggle*(-1)
            #If the touch sensor was pressed
            if self.touch.get_sample():
                #Brake left engine
                self.right.brake()
                #Brake right engine
                self.left.brake()
                #break the loop
                break

'''start using the code here for each task you will
need to start an object from the class Lego and connect to your robot with the function
lego.connect - fill in the name of your robot'''
# lego=Lego()
# lego.connect('_____')
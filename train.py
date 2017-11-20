class Train():

    #TODO: add fields for tipple state at arrival/departure

    def __init__(self, arrival_time, engines):
        self.arrival_time = arrival_time
        self.departure_time = 0
        self.wait_time = 0
        self.engines = engines

        if(engines == 5):
            self.capacity = 200.0
        else:
            self.capacity = 100.0
        self.loaded = 0.0
        #for tracking labor costs
        self.tipple_cost_at_exit = 0

    def get_arrival_time(self):
        return self.arrival_time

    def get_departure_time(self):
        return self.departure_time

    def get_wait_time(self):
        return self.wait_time

    def get_engines(self):
        return self.engines

    def get_capacity(self):
        return self.capacity

    def get_loaded(self):
        return self.loaded

    def get_tipple_cost_at_exit(self):
        return self.tipple_cost_at_exit

    def set_departure_time(self, time):
        self.departure_time = time

    def set_wait_time(self, time):
        self.wait_time = time

    def set_tipple_cost_at_exit(self, cost):
        self.tipple_cost_at_exit = cost


    def inc_wait_time(self, t):
        self.wait_time += t

    def inc_loaded(self, units):
        self.loaded += units

    def print_info(self):
        '''
        prints train information
        '''
        print "Engines: " + str(self.engines)
        print "Arrival Time: " + str(self.arrival_time)
        print "Departure Time: " + str(self.departure_time)
        print "Wait Time: " + str(self.wait_time)
        print "capacity: " + str(self.capacity)
        print "loaded: " + str(self.loaded)
        print ''

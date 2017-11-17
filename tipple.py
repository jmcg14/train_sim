class Tipple():

    def __init__(self):
        self.t_last_used = 0
        self.q_last_used = 0
        self.c_of_op = 0
        self.pay_rate1 = 9000.0/60.0
        self.pay_rate2 = 21000.0/60.0
        self.single_load_rate = 150.0/360.0
        self.capacity = 150.0

    def calc_tipple_load(self, t_current, num_crews):
        '''
        this method is used to calculate and update the tipple state at a given time.

        t_last_used = end time of previous train loading operation (minute)
        t_current = time of calculation (minute)
        q_last_used = quantity of coal remaining after last train load operation
        num_crew = number of crews that have been working to load tipple
        '''
        load_rate = self.single_load_rate*num_crews #quanity coal loaded by num crews
        period = t_current - self.get_t_last_used() #time spend loading
        cur_load = period*load_rate + self.get_q_last_used()

        if(cur_load > self.get_capacity()):
            cur_load = self.get_capacity()
        amnt_loaded = cur_load - self.get_q_last_used()

        cost = 0
        if(num_crews == 2):
            cost = (amnt_loaded/load_rate)*self.pay_rate2
        else:
            cost = (amnt_loaded/load_rate)*self.pay_rate1
        self.c_of_op += cost

        return cur_load

    def update_tipple(self, t, q):

        print '\ntipple updated: '
        print 't_new: ' + str(t)
        print 'q_new: ' + str(q)
        print ''

        self.t_last_used = t
        self.q_last_used = q

    def get_q_last_used(self):
        return self.q_last_used

    def get_t_last_used(self):
        return self.t_last_used

    #returns current value for cost of operation (c_of_op)
    def get_c_of_op(self):
        return self.c_of_op

    def get_capacity(self):
        return self.capacity

    def inc_c_of_op(self, cost):
        self.c_of_op += cost

    def calc_load_wait(self, q_to_fill, num_crews):
        #TODO: change to calculate to variable capacity rather than 100
        #q_to_fill is the quantity the train needs to be loaded.
        #max_time accounts for when q_to_fill exceeds tipple capacity
        base_load_rate = 150.0/360.0
        load_rate = base_load_rate*num_crews

        max_time = self.get_capacity()/load_rate
        #q_to_fill = q_target - self.get_q_last_used()
        time  = q_to_fill/load_rate

        #print '\nfrom calc load rate'
        #print 'time: ' + str(time) + ' rate: ' + str(load_rate)
        #print 'q_to_fill: ' + str(q_to_fill)
        #print 'amnt loaded : ' + str(time*load_rate)

        if(time>max_time):
            time = max_time
        return time

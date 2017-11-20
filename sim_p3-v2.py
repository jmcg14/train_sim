import numpy as np
import random
from tipple import Tipple
from train import Train
import train_stats

random.seed(0)

#TODO: DONE train loading time must be redefined in terms of train capacity to accomdate hi-capacity train
#TODO: DONE simulation must be extented to produce a weekly average for desired fields
#TODO: need to introduce means of varying crew_num throughout the day
#TODO: DONE calc_tipple_load in tipple.py needs to be refactored to incorporate cost calculations

def main():

    iterations = get_iteration_input()
    crews_available = get_crew_input()
    four_train = fourth_train_yes_or_no()
    output_dir = get_dir_input()
    file_name = get_fileName_input()

    run_sim(iterations, four_train, crews_available, output_dir, file_name)

def run_sim(iterations, four_train, crews_available, output_dir, file_name):
    days = iterations*364
    yearly_stats = []
    yearly_stats = sim_days(days, four_train, crews_available, yearly_stats)
    train_stats.write_to_file(iterations, output_dir, file_name, yearly_stats)

def sim_days(days, four_train, crews_available,  yearly_stats):
    std_arrivals = np.array([])
    xl_arrivals = np.array([])
    tipple = Tipple()
    trains = []
    num_trains = 3 #default

    #add fourth train
    if(four_train == True):
        print ('4 TRAINS')
        num_trains = 4

    weekly_trains = num_trains*7+1

    print ('num trains: ' + str(num_trains))
    #generates arrival times for each day -> day 0 is a sunday
    for day in range(0,days):
        std_arrivals = np.append(std_arrivals, gen_std_arrivals(day, num_trains))
        if(day%7 == 0):
            #generates arrival of high capacity train
            xl_arrival = random.uniform(660,780)+(1440*(day%7))+((day/7)*10080)
            xl_arrivals = np.append(xl_arrivals, int(round(xl_arrival)))

    #create list of all trains
    for x in std_arrivals:
        trains.append(Train(x, 3))
    for x in xl_arrivals:
        trains.append(Train(x, 5))

    #sort trains by arrival time
    trains = sorted(trains, key=lambda x: x.get_arrival_time())

    print ('ttl_trains ' + str(len(trains)/10))

    #calculates departure and wait times for every train in the list
    for index, train in enumerate(trains):
        if(train.get_arrival_time() < trains[index-1].get_departure_time()):
            train.inc_wait_time(trains[index-1].get_departure_time()-train.get_arrival_time())
        calc_departure(train, tipple, crews_available)

    #calculate figures for each iteration(year)
    i = 0
    while(i<(days/364)):
        ttl_trains_per_year = 52*weekly_trains
        print ('ttl_trains_per_year: ' + str(ttl_trains_per_year))
        base = ttl_trains_per_year*i
        weekly_dems = train_stats.weekly_demmurage_costs(trains[base:base+ttl_trains_per_year], i, weekly_trains)
        weekly_runover = train_stats.weekly_runover_time(trains[base:base+ttl_trains_per_year], i, weekly_trains)
        weekly_tipple_c = train_stats.weekly_tipple_cost(trains[base:base+ttl_trains_per_year], i, weekly_trains)

        print (np.shape(weekly_dems))
        print (np.shape(weekly_runover))
        print (np.shape(weekly_tipple_c))

        yearly_stats.append(np.array([weekly_dems, weekly_runover, weekly_tipple_c]))
        i+=1

    total_dems = 0

    yr_dem = 0
    for x in trains:
        yr_dem += calc_demurrage(train)

    print ('manual calculations: (debugging)')
    print ('total c_of_op ' + str(tipple.get_c_of_op()))
    print ('year 1 demmurage: ' + str(yr_dem))
    print ('total: ' + str(tipple.get_c_of_op()+yr_dem))
    print ('week1 end: ' + str(10080))
    print ('last train out: ' + str(trains[28].get_departure_time()))

    return yearly_stats

def gen_std_arrivals(day, num_trains):
    '''
    generates arrival times for standard trains (3 engines)
    arrival times are calculated within a continuous range of minutes
    60*24 = 1440 minutes in a day -> mod(1440)
    5:00 AM = 300
    8:00 PM = 20:00 = 1200
    generates arrival times on day x (x starts at 0)
    '''
    arrivals = np.array([])
    for x in range(0,num_trains):
        n = random.uniform(300, 1200)+(1440*day)
        arrivals = np.append(arrivals, int(round(n)))
    return np.sort(arrivals)

def calc_departure(train, tipple, crews_available):

    num_crews = crews_available #hardcoded temporarily
    train_load_rate = 100.0/180.0
    tipple_load_rate = tipple.get_capacity()/360.0

    #time at which train first arrives in postion to load
    load_start = train.get_arrival_time()+train.get_wait_time()

    #line below calculates loading occuring during idle time between trains
    #if no idle time the load_start == tipple.t_last_used and no changes are made
    cur_tipple_load = tipple.calc_tipple_load(load_start, num_crews)
    tipple.update_tipple(load_start, cur_tipple_load)

    #below while loop accomodates the hi_capcity trains that cannot be loaded all at once
    done = False
    departure = load_start
    while(not done):
        q_to_fill = train.get_capacity() - train.get_loaded()
        if(train.get_engines() == 5):
            if(cur_tipple_load >= q_to_fill):
                #if train can be loaded with what is currently in the tipple -> may never happen in current set up
                fill_time = q_to_fill/train_load_rate
                departure += fill_time
                train.inc_loaded(q_to_fill)
                done = True

            if(q_to_fill <= tipple.get_capacity()):
                #if the tipple can hold more than the train requires -> fill only whats needed to finish the train
                wait = tipple.calc_load_wait(q_to_fill, num_crews)
                cur_load = tipple.calc_tipple_load(tipple.get_t_last_used()+wait, num_crews)
                tipple.update_tipple(tipple.get_t_last_used()+wait, cur_load)
                train.inc_wait_time(wait)

                #once tipple is filled calculate departure time and update train
                fill_time = q_to_fill/train_load_rate
                departure += (wait+fill_time)
                train.inc_loaded(q_to_fill)
                tipple.update_tipple(tipple.get_t_last_used()+fill_time, 0)
                done = True

            else:
                #if not possible to fill in one go -> fill tipple completely
                q_to_fill = tipple.get_capacity() - tipple.get_q_last_used()
                wait = tipple.calc_load_wait(q_to_fill, num_crews)
                cur_load = tipple.calc_tipple_load(tipple.get_t_last_used()+wait, num_crews)
                tipple.update_tipple(tipple.get_t_last_used()+wait, cur_load)
                train.inc_wait_time(wait)

                #load entire tipple into train
                fill_time = tipple.get_q_last_used()/train_load_rate
                departure += (wait+fill_time)
                train.inc_loaded(tipple.get_q_last_used())
                tipple.update_tipple(tipple.get_t_last_used()+fill_time, 0)

        elif(train.get_engines() == 3):
            if(cur_tipple_load >= q_to_fill):
                #if regular train can be filled with whats currently in tipple
                fill_time = q_to_fill/train_load_rate
                departure = load_start + fill_time
            else:
                #tipple is filled only until train able to be loaded
                wait = tipple.calc_load_wait(q_to_fill - cur_tipple_load, num_crews)
                cur_load = tipple.calc_tipple_load(tipple.get_t_last_used()+wait, num_crews)
                tipple.update_tipple(tipple.get_t_last_used()+wait, cur_load)

                train.inc_wait_time(wait)

                #calculate fill and departure times
                fill_time = q_to_fill/train_load_rate
                departure = load_start + wait + fill_time

            #update tipple and train
            train.inc_loaded(q_to_fill)
            tipple.update_tipple(departure, tipple.get_q_last_used()-q_to_fill)
            done = True

    #train.set_tipple_cost_at_exit(tipple.get_c_of_op())
    train.set_departure_time(departure)
    return

def calc_demurrage(train):
    dem_rate = (train.get_engines()*5000.0)/60.0
    return train.get_wait_time()*dem_rate

def print_arrivals(trains, day):
    '''
    verbose output for debugging train arrival times
    '''
    print ("day: " + str(day))

    for train in trains:
        print ("train arrival: " + str(train.get_arrival_time()) + " arrival rel to day: " + str(train.get_arrival_time()%1440))

def print_results(trains, tipple, days):
    total_dem = 0
    for i, x in enumerate(trains):
        total_dem += calc_demurrage(x)

    print ('\ntotals:')
    print ('demurrage fees: ' + str(total_dem))
    print ('tipple cost of operation: ' + str(tipple.get_c_of_op()))
    print ('total cost of operation: ' + str(tipple.get_c_of_op() + total_dem))

    print ('\navg per week:')
    print ('demurage fees: ' + str(total_dem/((days/7)+1)))
    print ('tipple cost of operation: ' + str(tipple.get_c_of_op()/((days/7)+1)))
    print ('avg cost per week: ' + str((tipple.get_c_of_op() + total_dem)/((days/7)+1)))
    print ('')



#Function that will ask the user where their result folder is located at. 
def get_dir_input():
    print("Hi")

#Function that will ask the user what they want to name their output file as. 
#Output files will be given this name appended with the iteration number. 
def get_fileName_input():
    print("Hello")
	
	
#Function to see if the user wants to run sim with 4th daily train or not. 
def fourth_train_yes_or_no():
    four_train = True
    print("Would you like the simulation to run with three standard trains daily or four standard trains daily (Y/N): ")
    if(four_train == 'Y'):
      return True
    else:
      return False
	
#Function to get user input for the number of crews that they want to have for the simulation
def get_crew_input():
    ans = True
	
    while(ans==True):
      num_of_crews = int(input('Enter the number of Crews (1, 2, 3): '))
      if(num_of_crews != 1 and num_of_crews !=2 and num_of_crews != 3):
        print ('INVALID INPUT!\n')
      else:
        ans=False
    return num_of_crews

#Function to get user input for the number of iterations that they want the simulation to go through 
def get_iteration_input():
    ans = True

    while(ans==True):
      numI = int(input('Enter the number of iterations that you want the simulation to run for (1 - 10): '))
      if(numI != 1 and numI !=2 and numI != 3 and numI != 4 and numI !=5 and numI != 6 and  numI != 7 and numI !=8 and numI != 9 and numI != 10):
        print ('INVALID INPUT!\n')
      else:
        ans=False
    return numI
	
#Function to print cute train and welcome message 
def print_cute_train():
    print ("\n  _____                 . . . . . o o o o o")
    print ("__|[_]|__ ___________ _______    ____      o")
    print ("|[] [] []| [] [] [] [] [_____(__  ][]]_n_n__][.")
    print ("_|________|_[_________]_[________]_|__|________)<")
    print ("oo    oo 'oo      oo ' oo    oo 'oo 0000---oo\_")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("        WELCOME TO ASPEN-BOULDER COAL COMPANY")

if __name__=="__main__":
    main()

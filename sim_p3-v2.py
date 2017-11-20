import numpy as np
import random
from tipple import Tipple
from train import Train

random.seed(0)

#TODO: DONE train loading time must be redefined in terms of train capacity to accomdate hi-capacity train
#TODO: simulation must be extented to produce a weekly average for desired fields
#TODO: need to introduce means of varying crew_num throughout the day
#TODO: DONE calc_tipple_load in tipple.py needs to be refactored to incorporate cost calculations

def main():
    print_cute_train()
    option = menu()
    numI = get_interation_input()
    num_of_crews = get_crew_input()
    start_sim(option,numI,num_of_crews)
	
    #sim_days(42*2)

#Functiont that takes user input and starts sim based on their wants
def start_sim(option, numI, num_of_crews):

    if(option ==1):
      #Stick sim answer to first question here
      print("You have chosen option 1")
      #sim_days(1)
    elif(option == 2):
      #Stick sim answer to second question here
      print("You have chosen option 2")
      #sim_days(1)
    elif(option == 3):
      #Stick sim answer to third question here
      print("You have chosen option 3")
      #sim_days(1)
    elif(option == 4):
      #Stick sim answer to fourth question here
      print("You have chosen option 4")
      #sim_days(1)
    elif(option ==5):
      #Stick sim answer to 5th question here
      print("You have chosen option 5")
      #sim_days(1)
    else:
      #Stick sim answer to all questions here
      print("You have chosen option 6")
      #sim_days(1)


#Function to get user input for which question they would like answered. 
def menu():
    #print("=======================================================================================")
    print("\n\n\nYou have questions. We have the answers. ")
    print("Please select the question that you would like the answer too.")
    print("=======================================================================================")
    print("1. How often should the second crew be called out?")
    print("2. What are the expected monthly demurrage costs?")
    print("3. If the standard trains could be scheduled to arrive at precise times, ")
    print("   what daily schedule would minimze loading costs?")
    print("4. Would a third tipple-loading crew at $12,000 per hour reduce annual operations?")
    print("5. Can this tipple support a fouth standard train every day?")
    print("6. All")
    print("=======================================================================================\n")
	
    ans1 = True
	
    while(ans1==True):
      option = int(input('Please select an option (1,2,3,4,5,6): '))
      if(option != 1 and option !=2 and option != 3 and option != 4 and option != 5 and option != 6):
        print('INVALID INPUT!\n')
      else:
        ans1=False
    return option
	
#Function to get user input for the number of crews that they want to have for the simulation
def get_crew_input():
    ans = True
	
    while(ans==True):
      num_of_crews = int(input('Enter the number of Crews (1, 2, 3): '))
      if(num_of_crews != 1 and num_of_crews !=2 and num_of_crews != 3):
        print('INVALID INPUT!\n')
      else:
        ans=False
    return num_of_crews

#Function to get user input for the number of interations that they want the simulation to go through 
def get_interation_input():
    ans = True
	
    while(ans==True):
      numI = int(input('Enter the number of interations that you want the simulation to run for (1, 2, 3): '))
      if(numI != 1 and numI !=2 and numI != 3):
        print('INVALID INPUT!\n')
      else:
        ans=False
    return numI
#Function to print cute train and welcome message 
def print_cute_train():
    print("\n  _____                 . . . . . o o o o o")
    print("__|[_]|__ ___________ _______    ____      o")
    print("|[] [] []| [] [] [] [] [_____(__  ][]]_n_n__][.")
    print("_|________|_[_________]_[________]_|__|________)<")
    print("oo    oo 'oo      oo ' oo    oo 'oo 0000---oo\_")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("        WELCOME TO ASPEN-BOULDER COAL COMPANY")

def sim_days(days):
    std_arrivals = np.array([])
    xl_arrivals = np.array([])
    tipple = Tipple()
    trains = []

    #generates arrival times for each day -> day 0 is a sunday
    for day in range(0,days):
        std_arrivals = np.append(std_arrivals, gen_std_arrivals(day))
        if(day%7 == 0):
            #generates arrival of high capacity train
            xl_arrival = random.uniform(660,780)+(1440*day)+((day/7)*10080)
            xl_arrivals = np.append(xl_arrivals, int(round(xl_arrival)))

    for x in std_arrivals:
        trains.append(Train(x, 3))
    for x in xl_arrivals:
        trains.append(Train(x, 5))

    trains = sorted(trains, key=lambda x: x.get_arrival_time())


    #calculates departure and wait times for every train in the list
    for index, train in enumerate(trains):
        if(train.get_arrival_time() < trains[index-1].get_departure_time()):
            train.inc_wait_time(trains[index-1].get_departure_time()-train.get_arrival_time())
        calc_departure(train, tipple)

    print ('arrivals: ')
    print_arrivals(trains, 1)

    print ('\ntrains information: ')
    for train in trains:
        train.print_info()

    print_results(trains, tipple, days)

def gen_std_arrivals(day):
    '''
    arrival times are calculated within a continuous range of minutes
    60*24 = 1440 minutes in a day -> mod(1440)
    5:00 AM = 300
    8:00 PM = 20:00 = 1200
    generates arrival times on day x (x starts at 0)
    '''
    arrivals = np.array([])
    for x in range(1,4):
        n = random.uniform(300, 1200)+(1440*day)
        arrivals = np.append(arrivals, int(round(n)))
    return np.sort(arrivals)

def calc_departure(train, tipple):
    #BUG cur tipple load must be calculated based on start of load time, not arrival time FIXED
    #BUG: tipple must be updated after loading FIXED

    num_crews = 2 #hardcoded temporarily
    train_load_rate = 100.0/180.0
    tipple_load_rate = tipple.get_capacity()/360.0

    #time at which train first arrives in postion to load
    load_start = train.get_arrival_time()+train.get_wait_time()

    #below line calculates loading occuring during idle time between trains
    #if no idle time the load_start == tipple.t_last_used and no changes are made

    cur_tipple_load = tipple.calc_tipple_load(load_start, num_crews)
    tipple.update_tipple(load_start, cur_tipple_load)
    print ('')

    #below while loop accomodates the hi_capcity trains that cannot be loaded all at once
    done = False
    departure = load_start
    while(not done):
        q_to_fill = train.get_capacity() - train.get_loaded()
        if(train.get_engines() == 5):
            print ("\nbig train status: ")
            print ('cur_load: ' + str(train.get_loaded()))
            print ('q_to_fill: ' + str(q_to_fill))

            #if(cur_tipple_load >= q_to_fill):
                #if train can be loaded with what is currently in the tipple -> may never happen in current set up
            #    fill_time = q_to_fill/train_load_rate
            #    departure += fill_time
            #    train.inc_loaded(q_to_fill)
            #    done = True

            if(q_to_fill <= tipple.get_capacity()):
                #if possible fill tipple as much as required to finish train
                print ("\nbig ready to load(elif1): tipple state")
                print ("load start: " + str(load_start))
                print ("tipple_q_last: " + str(tipple.get_q_last_used()))
                print ("tipple_t_last: " + str(tipple.get_t_last_used()))

                wait = tipple.calc_load_wait(q_to_fill, num_crews)
                cur_load = tipple.calc_tipple_load(tipple.get_t_last_used()+wait, num_crews)
                tipple.update_tipple(tipple.get_t_last_used()+wait, cur_load)
                print ("\nbig train after waiting (elif1): ")
                print ("tipple_q_last: " + str(tipple.get_q_last_used()))
                print ("tipple_t_last: " + str(tipple.get_t_last_used()))
                print ("wait time: " + str(wait))


                train.inc_wait_time(wait)
                #once tipple is filled calculate departure time and update train
                fill_time = q_to_fill/train_load_rate
                departure += (wait+fill_time)
                train.inc_loaded(q_to_fill)
                tipple.update_tipple(tipple.get_t_last_used()+fill_time, 0)


                print ("big train second fill complete")
                print ("train cur_load: " + str(train.get_loaded()))
                print ("tipple_q_last: " + str(tipple.get_q_last_used()))
                print ("tipple_t_last: " + str(tipple.get_t_last_used()))

                done = True

            else:
                print ("big train ready to load(else)")
                print ("load start: " + str(load_start))
                print ("tipple_q_last: " + str(tipple.get_q_last_used()))
                print ("tipple_t_last: " + str(tipple.get_t_last_used()))
                print ('')

                #if not possible to fill in one go -> fill tipple completely
                q_to_fill = tipple.get_capacity() - tipple.get_q_last_used()
                wait = tipple.calc_load_wait(q_to_fill, num_crews)
                cur_load = tipple.calc_tipple_load(tipple.get_t_last_used()+wait, num_crews)
                tipple.update_tipple(tipple.get_t_last_used()+wait, cur_load)
                train.inc_wait_time(wait)

                print ("big train - first fill start: ")
                print ("tipple_q_last: " + str(tipple.get_q_last_used()))
                print ("tipple_t_last: " + str(tipple.get_t_last_used()))
                print ('')

                #load entire tipple into train
                fill_time = tipple.get_q_last_used()/train_load_rate
                departure += (wait+fill_time)
                train.inc_loaded(tipple.get_q_last_used())
                tipple.update_tipple(tipple.get_t_last_used()+fill_time, 0)

                print ("big train - first fill completed: ")
                print ("train cur_load: " + str(train.get_loaded()))
                print ("tipple_q_last: " + str(tipple.get_q_last_used()))
                print ("tipple_t_last: " + str(tipple.get_t_last_used()))

        elif(train.get_engines() == 3):
            print  ('\nregular train arrives - tipple state: ')
            print  ('t_last_used = ' + str(tipple.get_t_last_used()))
            print  ('q_last_used = ' + str(tipple.get_q_last_used()))

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
                print ('regular train after waiting for tipple to load:')
                print  ('t_last_used = ' + str(tipple.get_t_last_used()))
                print  ('q_last_used = ' + str(tipple.get_q_last_used()))

                #calculate fill and departure times
                fill_time = q_to_fill/train_load_rate
                departure = load_start + wait + fill_time

            #update tipple and train
            train.inc_loaded(q_to_fill)
            tipple.update_tipple(departure, tipple.get_q_last_used()-q_to_fill)
            print ('after train leaves - tipple update: ')
            print  ('t_last_used = ' + str(tipple.get_t_last_used()))
            print  ('q_last_used = ' + str(tipple.get_q_last_used()))
            print ('\n\n')
            done = True


    train.set_departure_time(departure)
    return

def calc_demurrage(train):
    dem_rate = (train.get_engines()*5000)/60
    return train.get_wait_time()*dem_rate

def print_day(trains, tipple):
    '''
    more verbose output for debugging daily calculations
    must be called within sim_day()
    '''
    print ("train 1 arrives: " + str(trains[0].get_arrival_time()))
    print ("train 1 departs: " + str(trains[0].get_departure_time()))
    print ("tipple state after train 1")
    print ("tipple t_last_used: " + str(tipple.get_t_last_used()))
    print ("tipple q_last_used: " + str(tipple.get_q_last_used()))

    print ('')

    print ("train 2 arrives: " + str(trains[1].get_arrival_time()))
    print ("train 2 departs: " + str(trains[1].get_departure_time()))
    print ("tipple state after train 2")
    print ("tipple t_last_used: " + str(tipple.get_t_last_used()))
    print ("tipple q_last_used: " + str(tipple.get_q_last_used()))

    print ('')

    print ("train 3 arrives: " + str(trains[2].get_arrival_time()))
    print ("train 3 departs: " + str(trains[2].get_departure_time()))
    print ("tipple state after train 3")
    print ("tipple t_last_used: " + str(tipple.get_t_last_used()))
    print ("tipple q_last_used: " + str(tipple.get_q_last_used()))

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


if __name__=="__main__":
    main()

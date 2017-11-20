import numpy as np
import os
import csv

def weekly_demmurage_costs(trains, i, n):
    '''
    this method generates a list containing the total demmurage fee for each
    week of the simulation
    i = current iteration
    n = number of trains per week
    '''
    dem = 0
    weekly_dems = np.array([])

    for index, train in enumerate(trains):
        if(index % n == 0):
            dem = 0
        dem += train.get_wait_time()*train.get_engines()*(5000.0/60.0)
        if(index % n == n-1):
            weekly_dems = np.append(weekly_dems, dem)
    return weekly_dems

def weekly_runover_time(trains, i, n):
    '''
    this method generates a list containing the number in minutes that weekly
    loading operations carry over into the following week.
        because this simulation is continuous over multiple iterations(years) the current
    iteration (i) is supplied for calulations to be accurate.
    '''

    t = 1440*7 #number of minutes in a week
    t_yr = t*52 #minutes in a year
    weekly_runover = np.array([])

    for index, train in enumerate(trains):
        week = index/n+1
        if(index % n == n-1):
            week_finish = week*t
            runover = train.get_departure_time() - (week_finish+(t_yr*i))

            if(runover < 0):
                runover = 0

            weekly_runover = np.append(weekly_runover, runover)
    return weekly_runover

def weekly_tipple_cost(trains, i, n):
    '''
    calculates the cost of tipple loading operations for each week.
    note: this funcitons output has unresolved bugs, calculating weekly avg based
    on final tipple_cost instead
    '''
    tipple_cost = np.array([])

    for index, train in enumerate(trains):
        week = index/n+1

        if(index % n == n-1):
            if(index == n-1):
                tipple_cost = np.append(tipple_cost, train.get_tipple_cost_at_exit())
            else:
                tipple_cost = np.append(tipple_cost, train.get_tipple_cost_at_exit()-tipple_cost[-1])

    return tipple_cost


def write_to_file(iteration, output_dir, file_name, stats):

    stats = np.array(stats)
    path1 = output_dir+file_name

    for i,x in enumerate(stats):
        path = path1 + str(i+1) + '.csv'
        with open(path, 'wb') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONE)
            writer.writerow(["week","demmurage_costs", "runover_time", "tipple_cost"])
            for j,y in enumerate(x[0]):
                writer.writerow([j+1, x[0][j], x[1][j], x[2][j]])

    return

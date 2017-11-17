import numpy as np

def weekly_demmurage_costs(trains):
    '''
    this method generates a list containing the total demmurage fee for each
    week of the simulation
    '''
    n = 22 #trains arriving per week
    dem = 0
    weekly_dems = np.array([])
    for index, train in enumerate(trains):
        if(index % 22 == 0 and index != 0):
            weekly_dems = np.append(weekly_dems, dem)
            dem = 0
        dem += train.get_wait_time()*train.get_engines()*(5000.0/60.0)
    return weekly_dems

def weekly_runover_time(trains):
    '''
    this method generates a list containing the number in minutes that weekly
    loading operations carry over.
    '''
    n = 22 #trains arriving per weekly
    t = 1440*7 #number of minutes in a week
    weekly_runnover = np.array([])

    for index, train in enumerate(trains):
        week = (index/21)+1
        if(index % 22 == 21 and index != 0):
            week_finish = train.get_departure_time()
            weekly_runnover = np.append(weekly_runnover, week_finish)
    return weekly_runnover

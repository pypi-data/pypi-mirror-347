import datetime

def date_str(full_month_name:bool=False) -> str:
    '''Return the current date
    
    Args
    ----
    full_month_name (bool): Flag to return full month string.
    
    Returns
    ---
    day_string (str): Day in format YYYYMMMDD
    '''
    current_time = datetime.datetime.now()

    if full_month_name:
        day_string = "%s%s%s"%(current_time.strftime("%Y"), 
                               current_time.strftime("%B").lower(),
                               current_time.strftime("%d"))
    else:
        day_string = "%s%s%s"%(current_time.strftime("%Y"),  
                               current_time.strftime("%b").lower(), 
                               current_time.strftime("%d"))
    return day_string


def time_str() -> str:
    '''Return the current date
    
    Returns
    ---
    time_string (str): Time in 24 hour clock in format HHMM
    '''
    current_time = datetime.datetime.now()

    time_string = "%s%s"%(current_time.strftime("%H"), 
                          current_time.strftime("%M"))
    return time_string


def date_and_time(full_month_name:bool=False) -> str:
    '''Return the current date and time.
    
    Args
    ----
    full_month_name (bool): Flag to return full month string.
    
    Returns
    ---
    day_string (str): Day in format YYYYMMMDD
    
    time_string (str): Time in 24 hour clock in format HHMM
    '''
    return "%s_%s"%(date_str(full_month_name), time_str())


from datetime import datetime,timedelta

def time():
    x=datetime(2022,10,1)-timedelta(days=1)
    print(x)
time()
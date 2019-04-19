import datetime
import time
#from threading import Timer

# x=datetime.today()
# y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
# delta_t=y-x
# print(delta_t)

# secs=delta_t.seconds+1

# print(secs)

next_start = datetime.datetime(2019, 4, 19, 14, 38, 0)
while True:
    dtn = datetime.datetime.now()

    if dtn >= next_start:
        next_start += datetime.timedelta(1)  # 1 day
        # do what needs to be done
        print('send out reminder!')
    else:
    	print(dtn)
    	print(next_start)

    time.sleep(5)
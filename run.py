from crontab import CronTab
from endsars import Endsars
try:
    Endsars()
except:
    Endsars()

# from crontab import CronTab
#
# cron = CronTab(user='arah')
# job = cron.new(command='endsars.py')
# job.hour.every(1)
# cron.write()

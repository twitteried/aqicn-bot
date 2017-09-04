# aqicn-bot

A trivial Twitter bot that pulls air pollution data from aqicn.org and tweets
about it.

It seems best to run it with cron at the 30th minute of every hour, because
while aqicn.org updates every hour, the update won't often populate until after
15 minutes or more has passed.  

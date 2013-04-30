import MinionCollective
import gc
import time

minionCollective = MinionCollective.MinionCollective()
cycles = 0

while True:
	job = minionCollective.getJob()
	if job is None:
		job = minionCollective.getExpiredJob()
	if job is None:
		cycles += 1
		if cycles > 30:
			minionCollective.removeJobs()
			gc.collect()
		time.sleep(10)
	else:
		if job['action'] == 'action1':
			#call the function here
			pass
		elif job['action'] == 'action2':
			pass
		minionCollective.finishJob(job['_id'])
import MinionCollective
import gc
import time

minionCollective = MinionCollective.MinionCollective()
cycles = 0

while True:
	job = minionCollective.get_job()
	if job is None:
		job = minionCollective.get_expired_job()
	if job is None:
		cycles += 1
		if cycles > 30:
			minionCollective.remove_jobs()
			gc.collect()
		time.sleep(10)
	else:
		if job['action'] == 'action1':
			#call the function here
			pass
		elif job['action'] == 'action2':
			pass
		minionCollective.finish_job(job['_id'])
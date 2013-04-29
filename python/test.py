import MinionCollective
import time

timeout = 1
minionCollective = MinionCollective.MinionCollective(timeout)


if minionCollective.getJobCount() is 0:
	print "No Jobs in DB"
	print "Tests Initialising"

	minionCollective.addJob('doSomething', 1)
	job = minionCollective.getJob()

	if job['action'] == 'doSomething' and job['id'] == 1:
		print "Add and Get Job Test Passed"
	else:
		print "Add and Get Job Test Failed"

	time.sleep(timeout + 1)

	job = minionCollective.getExpiredJob()
	if job['action'] == 'doSomething' and job['id'] == 1:
		print "Get Expired Job Test Passed"
	else:
		print "Get Expired Job Test Failed"

	job = minionCollective.finishJob(job['_id'], True)
	if job['status'] == 'C':
		print "Finish Job Test Passed"
	else:
		print "Finish Job Test Failed"

	minionCollective.removeJobs()
	if minionCollective.getJobCount() is 0:
		print "Remove Job Test Passed"
	else:
		print "Remove Job Test Failed"


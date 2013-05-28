import MinionCollective
import time

timeout = 1
minionCollective = MinionCollective.MinionCollective(timeout)


if minionCollective.get_job_count() == 0:
	print "No Jobs in DB"
	print "Tests Initialising"

	minionCollective.add_job('doSomething', 1)
	job = minionCollective.get_job()

	if job['action'] == 'doSomething' and job['id'] == 1:
		print "Add and Get Job Test Passed"
	else:
		print "Add and Get Job Test Failed"

	time.sleep(timeout + 1)

	job = minionCollective.get_expired_job()
	if job['action'] == 'doSomething' and job['id'] == 1:
		print "Get Expired Job Test Passed"
	else:
		print "Get Expired Job Test Failed"

	job = minionCollective.finish_job(job['_id'], True)
	if job['status'] == 'C':
		print "Finish Job Test Passed"
	else:
		print "Finish Job Test Failed"

	minionCollective.remove_jobs()
	if minionCollective.get_job_count() == 0:
		print "Remove Job Test Passed"
	else:
		print "Remove Job Test Failed"

	minionCollective.add_job('doSomething', 1)
	job = minionCollective.get_job('doOtherThing')
	if job == None:
		print "Incorrect Get Job Test Passed"
	else:
		print "Incorrect Get Job Test Failed"

	job = minionCollective.get_job('doSomething')

	if job['action'] == 'doSomething' and job['id'] == 1:
		print "Valid Get Job Test Passed"
	else:
		print "Valid Get Job Test Failed"

	time.sleep(timeout + 1)

	job = minionCollective.get_expired_job()
	if job['action'] == 'doSomething' and job['id'] == 1:
		print "Get Expired Job Test Passed"
	else:
		print "Get Expired Job Test Failed"

	job = minionCollective.finish_job(job['_id'], True)
	if job['status'] == 'C':
		print "Finish Job Test Passed"
	else:
		print "Finish Job Test Failed"

	minionCollective.remove_jobs()
	if minionCollective.get_job_count() == 0:
		print "Remove Job Test Passed"
	else:
		print "Remove Job Test Failed"
import pymongo;
from time import time


class MinionCollective:
	def __init__(self, timeout = 60, dbName = 'MinionCollective', taskPoolName = 'queue', mongoURI = 'mongodb://localhost:27017'):
		self._timeout = timeout
		self._dbName = dbName
		self._taskPoolName = taskPoolName
		self._mongoURI = mongoURI
		self._conn = self._connectServer()

	def addJob(self, action, id, data = ''):
		job = {
			'action'		: action,
			'id'			: id,
			'data'			: data,
			'status'		: 'W',
			'last_update'	: int(time())
		}
		if self._conn.alive():
			return self._connectCollection().insert(job)
		else:
			return False

	def getJob(self, action = None):
		if action == None:
			job = {'status' : 'W'}
		else:
			job = {
				'status' : 'W',
				'action' : action
			}
		modify = {
			'$set' : {
				'status' : 'I',
				'last_update' : int(time())
			}
		}

		if self._conn.alive():
			return self._connectCollection().find_and_modify(job, modify, False, [('last_update', 1)])
		else:
			return False

	def getExpiredJob(self):
		job = {
			'status' : 'I',
			'last_update' : {
				'$lt' : int(time()) - self._timeout
			}
		}
		modify = {
			'$set' : {
				'status' : 'I',
				'last_update' : int(time())
			}
		}
		if self._conn.alive():
			return self._connectCollection().find_and_modify(job, modify, False, [('last_update', 1)])
		else:
			return False

	def finishJob(self, id, newVar = False):
		job = {
			'_id' : id
		}
		modify = {
			'$set' : {
				'status' : 'C',
				'last_update' : int(time())
			}
		}

		if self._conn.alive():
			return self._connectCollection().find_and_modify(job, modify, False, None, False, new=newVar)
		else:
			return False

	def removeJobs(self):
		job = {
			'status' : 'C'
		}
		if self._conn.alive():
			return self._connectCollection().remove(job)
		else:
			return False

	def getJobCount(self):
		if self._conn.alive():
			return self._connectCollection().count()
		else:
			return False

	def _connectServer(self):
		return pymongo.MongoClient(self._mongoURI);

	def _connectCollection(self):
		return self._conn[self._dbName][self._taskPoolName]


import pymongo;
from time import time


class MinionCollective:
	def __init__(self, timeout = 60, dbName = 'MinionCollective', taskPoolName = 'queue', mongoURI = 'mongodb://localhost:27017', replicaSet = None):
		self._timeout = timeout
		self._dbName = dbName
		self._taskPoolName = taskPoolName
		self._mongoURI = mongoURI
		self._replicaSet = replicaSet
		if replicaSet == None:
			self._conn = self._connectServer()
		else:
			self._conn = self._connectReplicaSet()

	def addJob(self, action, id, data = ''):
		job = {
			'action'		: action,
			'id'			: id,
			'data'			: data,
			'status'		: 'W',
			'last_update'	: int(time())
		}
		return self._connectCollection().insert(job)

	def getJob(self, action = None):
		if action == None:
			job = {'status' : 'W'}
		else:
			job = {
				'status' : 'W',
				'action' : action
			}
		print type(job)
		modify = {
			'$set' : {
				'status' : 'I',
				'last_update' : int(time())
			}
		}
		return self._connectCollection().find_and_modify(job, modify, False, [('last_update', 1)])

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
		return self._connectCollection().find_and_modify(job, modify, False, [('last_update', 1)])

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
		return self._connectCollection().find_and_modify(job, modify, False, None, False, new=newVar)

	def removeJobs(self):
		job = {
			'status' : 'C'
		}
		return self._connectCollection().remove(job)

	def getJobCount(self):
		return self._connectCollection().count()


	def _connectServer(self):
		return pymongo.MongoClient(self._mongoURI);

	def _connectReplicaSet(self):
		return pymongo.MongoReplicaSetClient(self._mongoURI, self._replicaSet);

	def _connectCollection(self):
		if not self._conn.alive():
			if self._replicaSet == None:
				self._conn = self._connectServer()
			else:
				self._conn = self._connectReplicaSet()
		return self._conn[self._dbName][self._taskPoolName]



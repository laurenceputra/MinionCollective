import pymongo;
import mongodb_proxy;
from time import time


class MinionCollective:
	def __init__(self, timeout = 60, dbName = 'MinionCollective', taskPoolName = 'queue', mongoURI = 'mongodb://localhost:27017', replicaSet = None):
		self._timeout = timeout
		self._dbName = dbName
		self._taskPoolName = taskPoolName
		self._mongoURI = mongoURI
		self._replicaSet = replicaSet
		if replicaSet == None:
			self._conn = self._connect_server()
		else:
			self._conn = self._connectReplicaSet()

	def add_job(self, action, id, data = ''):
		job = {
			'action'		: action,
			'id'			: id,
			'data'			: data,
			'status'		: 'W',
			'last_update'	: int(time())
		}
		return self._connect_collection().insert(job)

	def get_job(self, action = None):
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
		return self._connect_collection().find_and_modify(job, modify, False, [('last_update', 1)])

	def get_expired_job(self):
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
		return self._connect_collection().find_and_modify(job, modify, False, [('last_update', 1)])

	def finish_job(self, id, newVar = False):
		job = {
			'_id' : id
		}
		modify = {
			'$set' : {
				'status' : 'C',
				'last_update' : int(time())
			}
		}
		return self._connect_collection().find_and_modify(job, modify, False, None, False, new=newVar)

	def remove_jobs(self):
		job = {
			'status' : 'C'
		}
		return self._connect_collection().remove(job)

	def get_job_count(self):
		return self._connect_collection().count()


	def _connect_server(self):
		return mongodb_proxy.MongoProxy(pymongo.MongoClient(self._mongoURI));

	def _connect_replica_set(self):
		return mongodb_proxy.MongoProxy(pymongo.MongoReplicaSetClient(self._mongoURI, self._replicaSet));

	def _connect_collection(self):
		if not self._conn.alive():
			if self._replicaSet == None:
				self._conn = self._connect_server()
			else:
				self._conn = self._connectReplicaSet()
		return self._conn[self._dbName][self._taskPoolName]



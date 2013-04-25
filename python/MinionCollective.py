import pymongo;
from time import time


class MinionCollective:
	def __init__(self, timeout = 60, dbName = 'MinionCollective', taskPoolName = 'queue', mongoURI = 'mongodb://localhost:27017'):
		self._timeout = timeout
		self._dbName = dbName
		self._taskPoolName = taskPoolName
		self._mongoURI = mongoURI

	def addJob(self, action, id, data = ''):
		job = {
			'action'		: action,
			'id'			: id,
			'data'			: data,
			'status'		: 'W',
			'last_update'	: int(time())
		}
		collection = self._connectCollection()
		return collection.insert(job)

	def _connectDB(self):
		return pymongo.MongoClient(self._mongoURI);

	def _connectCollection(self):
		conn = self._connectDB()
		return conn[self._dbName][self._taskPoolName]


	_timeout = 60
	_dbName = 'MinionCollective'
	_taskPoolName = 'queue'
	_mongoURI = 'mongodb://localhost:27017'

mongo = MinionCollective();
mongo.addJob("Sing", 1)
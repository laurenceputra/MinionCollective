<?php
/**
* MinionCollective class
* Allows you to interact with the distributed task pool
*/
class MinionCollective{
	function __construct(){
		//Maximum execution time before regarded as failure in seconds
		$this->timeout = 60;
		//Collection name of task pool
		$this->taskPoolName = 'queue';
		//Connection string, in the form 'mongodb://[username:password@]host1[:port1][,host2[:port2:],...]/db'
		$this->mongoURI = 'mongodb://localhost:27017';
		//Connection options
		$this->mongoOptions = array('db' => 'MinionCollective');
	}

	/******************
	 * Adds a job into the task pool
	 * Takes in an action, identifier, as well as data concerning the job
	 * Data can be anything (string, array), as long as size of $job is less than 4MB
	 * Returns an array with the results of the insert
	******************/
	public function addJob($action, $id, $data = ''){
		$job = array('action' => $action, 'id' => $id, 'data' => $data, 'status' => 'W', 'last_update' => time());
        $collection = $this->connectCollection();
        return $collection->insert($job);
	}

	/******************
	 * Pulls out the oldest undone job from the task pool
	 * Returns an array representing the job that was inserted
	 * Array has the indexes 'action', 'id', 'data', specified when adding job
	 * In addition, there is a '_id' index to be used when reporting the end of job
	******************/
	public function getJob(){
		$job = array('status' => 'W');
        $modify = array('$set' => array('status' => 'I', 'last_update' => time()));
        $options = array('sort' => array("last_update" => 1));
		$collection = $this->connectCollection();
		return $collection->findAndModify($job, $modify, null, $options);
	}

	/******************
	 * Identical to getJob, except it pulls out jobs that are suspected of having crashed
	******************/	
	public function getExpiredJob(){
		$job = array('status' => 'I', 'last_update' => array('$lt' => time() - $this->timeout));
        $modify = array('$set' => array('status' => 'I', 'last_update' => time()));
        $options = array('sort' => array("last_update" => 1));
		$collection = $this->connectCollection();
		return $collection->findAndModify($job, $modify, null, $options);
	}

	/******************
	 * Specifies a job as finished
	 * Returns an array representing the job that was inserted
	******************/
	public function finishJob($id){
        $job = array('_id' => $id);
        $modify = array('$set' => array('status' => 'C', 'last_update' => time()));
        $collection = $this->connectCollection();
        return $collection->findAndModify($job, $modify);
    }

    /******************
	 * Removes all completed jobs
	******************/
	public function removeJob(){
        $job = array('status' => 'C');
        $collection = $this->choose_collection();
        $collection->remove($job);
    }

    private function connectDB(){
		return new MongoClient($this->mongoURI, $this->mongoOptions);
	}

	private function connectCollection(){
		$collectionName = $this->taskPoolName;
		return $this->connectDB()->MinionCollective->queue;
	}

	private $timeout;
	private $taskPoolName;
	private $mongoURI;
	private $mongoOptions;
}


?>
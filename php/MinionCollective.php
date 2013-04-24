<?php
/**
* MinionCollective class
* Allows you to interact with the distributed task pool
*/
class MinionCollective{

	/******************
	 * Creates the MinionCollective Object
	 * Takes in timeout, dbName, taskPoolName, mongoURI, and mongooptions
	 * timeout is the maximum execution time before regarded as failure in seconds
	 * dbName is name of the database that will be used
	 * taskPoolName is the name of the collection that will be used
	 * mongoURI is connection string used to connect to MongoDB
	 * mongoOptions is an array containing the options for connecting to MongoDB
	******************/
	function __construct($timeout = 60, $dbName = 'MinionCollective', $taskPoolName = 'queue', $mongoURI = 'mongodb://localhost:27017', $mongoOptions = array()){
		$this->timeout = $timeout;
		$this->taskPoolName = $taskPoolName;
		$this->dbName = $dbName;
		$this->mongoURI = $mongoURI;
		$this->mongoOptions = $mongoOptions;
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
	public function getExpiredJob($timeout = -1){
		if($timeout == -1){
			$timeout = $this->timeout;
		}
		$job = array('status' => 'I', 'last_update' => array('$lt' => time() - $timeout));
        $modify = array('$set' => array('status' => 'I', 'last_update' => time()));
        $options = array('sort' => array("last_update" => 1));
		$collection = $this->connectCollection();
		return $collection->findAndModify($job, $modify, null, $options);
	}

	/******************
	 * Specifies a job as finished
	 * Returns an array representing the job that was inserted
	******************/
	public function finishJob($id, $new = FALSE){
        $job = array('_id' => $id);
        $modify = array('$set' => array('status' => 'C', 'last_update' => time()));
        $options = array('new' => $new);
        $collection = $this->connectCollection();
        return $collection->findAndModify($job, $modify, NULL, $options);
    }

    /******************
	 * Removes all completed jobs
	******************/
	public function removeJobs(){
        $job = array('status' => 'C');
        $collection = $this->connectCollection();
        $collection->remove($job);
    }

    public function getJobCount(){
    	return $this->connectCollection()->count();
    }

    private function connectDB(){
		return new MongoClient($this->mongoURI, $this->mongoOptions);
	}

	private function connectCollection(){
		$conn = $this->connectDB();
		$collectionName = $this->taskPoolName;
		if(is_a($conn, 'MongoClient')){
			$dbName = $this->dbName;
			return $conn->$dbName->$collectionName;
		}
		else{
			return $conn->$collectionName;
		}
		
		return $this->connectDB()->MinionCollective->queue;
	}

	private $timeout;
	private $taskPoolName;
	private $mongoURI;
	private $mongoOptions;
	private $dbName;
}


?>
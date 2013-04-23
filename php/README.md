# PHP Minion Collective Class

This is the PHP version of the Minion Collective. Simply import MinionCollective.php in your code to start using it.

## Requirements

    PHP MongoDB driver
    
## How to use

You will have to set up the following variables in the MinionCollective.php file. The default set of settings should work for most normal setups.

    private $timeout
	private $taskPoolName
	private $mongoURI
	private $mongoOptions

After that, include the following 2 lines just before you want to start using the MinionCollective

    require_once('MinionCollective.php');
    $minionCollective = new MinionCollective();


### Adding jobs to the task pool

After including the MinionCollective file, as well as creating the object, adding a task is as simple as doing

    $minionCollective->addJob($action, $id, $data)

$action is the action of that job.

$id is the identifier of that job, some piece of information that can identify that job and is absolutely necessary

$data is any additional information you'll need to ensure the job gets completed

### Running workers to do the jobs

Minion.php is precisely that. It is designed to be as lightweight as possible, and it's only role is to clear as many task as it can from the task pool. Note that you can run as many minions on as many machines as you want, and they will start clearing the jobs in the task pool.

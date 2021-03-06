# PHP Minion Collective Class

This is the PHP version of the Minion Collective. Simply import MinionCollective.php in your code to start using it.

## Requirements

1. PHP MongoDB driver
2. A MongoDB Database/Cluster

## How to use

Include the following 2 lines just before you want to start using the MinionCollective

    require_once('MinionCollective.php');
    $minionCollective = new MinionCollective();

MinionCollective takes in the following arguments with default values

    MinionCollective($timeout = 60, $dbName = 'MinionCollective', $taskPoolName = 'queue', $mongoURI = 'mongodb://localhost:27017', $mongoOptions = array())

### Adding jobs to the task pool

After including the MinionCollective file, as well as creating the object, adding a task is as simple as doing

    $minionCollective->addJob($action, $id, $data)

$action is the action of that job.

$id is the identifier of that job, some piece of information that can identify that job and is absolutely necessary

$data is any additional information you'll need to ensure the job gets completed

### Running workers to do the jobs

Minion.php is precisely that. It is designed to be as lightweight as possible, and it's only role is to clear as many tasks as it can from the task pool. Note that you can run as many minions on as many machines as you want, and they will start clearing the jobs in the task pool.

Of course you will first have to specify what task it should run, but that can be added into the code without causing much changes in the memory footprint using [exec](http://www.php.net/manual/en/function.exec.php) or [system](http://php.net/manual/en/function.system.php).

Run it from the commandline and send it to the background by simply doing the following

    php Minion.php &
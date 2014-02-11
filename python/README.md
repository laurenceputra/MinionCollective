# Python MinionCollective

## Requirements

1. pymongo
2. A MongoDB Database/Cluster

## How to use

Include the following 2 lines just before you want to start using the MinionCollective

    import MinionCollective
    minionCollective = MinionCollective.MinionCollective()

MinionCollective takes in the following arguments with default values

    MinionCollective(timeout = 60, dbName = 'MinionCollective', taskPoolName = 'queue', mongoURI = 'mongodb://localhost:27017', replicaSet = None)

### Adding jobs to the task pool

After including the MinionCollective file, as well as creating the object, adding a task is as simple as doing

    minionCollective.addJob(action, id, data)

action is the action of that job.

id is the identifier of that job, some piece of information that can identify that job and is absolutely necessary

data is any additional information you'll need to ensure the job gets completed

### Running workers to do the jobs

Minion.py is precisely that. It is designed to be as lightweight as possible, and it's only role is to clear as many tasks as it can from the task pool. Note that you can run as many minions on as many machines as you want, and they will start clearing the jobs in the task pool.

Of course you will first have to specify what task it should run, but that can be added into the code without causing much changes in the memory footprint using [subprocess](http://docs.python.org/2/library/subprocess.html) or [system](http://docs.python.org/2/library/os.html#os.system).

Run it from the commandline and send it to the background by simply doing the following

    python Minion.py &

## Projects used

MinionCollective's Python version uses the mongodb_proxy coded by Gustav Arngården. The original blogpost regarding that can be found over at http://www.arngarden.com/2013/04/29/handling-mongodb-autoreconnect-exceptions-in-python-using-a-proxy


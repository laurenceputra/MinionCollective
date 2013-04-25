<?php
require_once('MinionCollective.php');

$timeout = 1;

$minionCollective = new MinionCollective($timeout, 'MinionCollective', 'queue');

if($minionCollective->getJobCount() == 0){
    echo "No Jobs in DB".PHP_EOL;
    echo "Tests Initialising".PHP_EOL;
    $minionCollective->addJob('doSomething', 1);
    $job = $minionCollective->getJob();

    //verify that contents of job are the same
    echo "Add and Get Job Test ";
    if($job['action'] == 'doSomething' && $job['id'] == 1){
        echo "Passed".PHP_EOL;
    }
    else{
        echo "Failed".PHP_EOL;
    }

    sleep($timeout + 1);

    echo "Get Expired Job Test ";
    $job = $minionCollective->getExpiredJob();
    if($job['action'] == 'doSomething' && $job['id'] == 1){
        echo "Passed".PHP_EOL;
    }
    else{
        echo "Failed".PHP_EOL;
    }

    echo "Finalise Job Test ";
    $job = $minionCollective->finishJob($job['_id'], TRUE);
    if($job['status'] == 'C'){
        echo "Passed".PHP_EOL;
    }
    else{
        echo "Failed".PHP_EOL;
    }

    echo "Remove Job Test ";
    $minionCollective->removeJobs();
    if($minionCollective->getJobCount() == 0){
        echo "Passed".PHP_EOL;
    }
    else{
        echo "Failed".PHP_EOL;
    }
}
else{
    echo "Database has existing jobs";
}


?>
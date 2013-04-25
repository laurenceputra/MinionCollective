<?php
require_once('MinionCollective.php');

$minionCollective = new MinionCollective();
$cycles = 0;

while(true){
    $job = $minionCollective->getJob();
    if($job == NULL){
        $job = $minionCollective->getExpiredJob();
    }
    if(!$job){
        $cycles++;

        // Add in other stuff here to do in case there are no jobs available

        if($cycles > 30){
            $cycles = 0;
            $minionCollective->removeJobs();
            gc_collect_cycles();
        }
        sleep(10);
    }
    else{
        if($job['action'] == 'action1'){
            //do something
            exec('/usr/bin/echo Action1');
        }
        else if($job['action'] == 'action2'){
            //do something
            exec('/usr/bin/echo Action2');
        }
        $minionCollective->finishJob($job['_id']);
        $job = NULL;
        unset($job);
    }
}

?>
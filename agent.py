
import os
import sys
import subprocess
import glob
import logging
import workflow
import settings
import time

#
#   This class is the main entry point for the solution
#   The Agent class implements the functionality
#   check the main class for the command line arguments, or type agent -h
#



#sets up the debug level
#TODO:this should be moved or read from a config file or entry parameter
logging.basicConfig(filename=settings.agent_path+'/agent.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Agent(object):

    """Implements job monitoring"""
    def __init__(self):
        sys.path = [settings.modules_path] + sys.path
        sys.path = [settings.agent_path] + sys.path
        sys.path = [settings.workflows_path] + sys.path

    def modules(self):
        modules = glob.glob(settings.modules_path+'/*.py')
        return [x[len(settings.modules_path)+1:-3] for x in modules]

    def workflows(self):
        work = glob.glob(settings.workflows_path+'/*.py')
        return [x[len(settings.workflows_path)+1:-3] for x in work]

    def datasets(self):
        out = subprocess.check_output(["ls", "--color=never", "datasets"])
        files = out.split()
        return files

    def progress(self, job_id):
        return 0.42

    def scheduleWorkflow(self, workflowName):
        flow = workflow.Workflow(agent.id_increment_and_get(), workflowName)
        flow.launch()
        return flow.id

    def testWorkflow(self, workflowName):
        try:
            flow = workflow.Workflow(0, workflowName,'test')
            print(flow)
        except Exception as e:
            print(e)
            logging.exception(e)

    def finishWorkflow(self, workflowDir):
        return True

    def report(self, jobId):
        print("generating report...")
        print("done")


    def updateState(self, job_id):
        logging.info("updating state of workflow:{}".format(job_id))
        flow = workflow.from_id(job_id)
        flow.updateState()

    def id_increment_and_get(self):
        state_file = None
        if (not os.path.exists(settings.persistent_state_path)):
            state_file = open(settings.persistent_state_path,  'w')
            state_file.write(str(0))
            state_file.close()
            return 0
        else:
            state_file = open(settings.persistent_state_path, 'r')
            id = int(state_file.read()) + 1
            state_file.close()
            state_file = open(settings.persistent_state_path, 'w')
            state_file.write(str(id))
            return id

if __name__ == "__main__":
    logging.info("NEW RUN: called agent with: "+repr(sys.argv))
#    print(sys.version_info)

    #wait on file lock
    #this sucks, I know it, you know it, lets just ignore it, hopefully it will go away eventually (it likely wont)
    #the lock is needed because we want to run just a single instance of agent at a time, as it mutates state.
    #however, we do not want the process to simply exit if another process has called agent because
    #we have some tasks issue an update order on completion which we don't want to lose
    #(it would not be a fatal error if we lose the update, but it sucks nonetheless, as we must now wait for the watchdog)
    #the lock is removed in the finally clause
    while(True):
        if os.path.exists(settings.global_filelock_path):
            logging.info("lock exists. is another instance running? waiting a bit...")  #remove print after test
            logging.info("this was caused by running: "+repr(sys.argv))
            time.sleep(1)
        else:
            lock = open(settings.global_filelock_path, "w")
            lock.close()
            break

    agent = Agent()
    try:

        i = 1
        while i < len(sys.argv):
            if(sys.argv[i] == "-m"):
                logging.info("called agent with -m (request modules)")
                for item in agent.modules():
                    print(item)
                i += 1
                continue

            if(sys.argv[i] == "-w"):
                logging.info("called agent with -w (request workflows)")
                for item in agent.workflows():
                    print(item)
                i += 1
                continue

            if(sys.argv[i] == "-s" and i+1 < len(sys.argv)):
                logging.info("called agent with -s (schedule workflow):"+sys.argv[i+1])
                agent.scheduleWorkflow(sys.argv[i+1])
                i += 2
                continue

            if(sys.argv[i] == "-t" and i+1 < len(sys.argv)):
                logging.info("called agent with -t (test workflow):"+sys.argv[i+1])
                agent.testWorkflow(sys.argv[i+1])
                i += 2
                continue

            if(sys.argv[i] == "-u" and i+1 < len(sys.argv)):
                logging.info("called agent with -u (update state):"+sys.argv[i+1])
                task_id = agent.updateState(int(sys.argv[i+1]))
                print(id)
                i += 2
                continue

            if(sys.argv[i] == "-ud" and i+1 < len(sys.argv)):
                logging.info("called agent with -ud (update state with directory):"+sys.argv[i+1])
                #extract workflow id from directory
                path = sys.argv[i+1].rstrip(os.sep)
                logging.info(path)
                logging.info(path.split(os.sep))
                path_component = path.split(os.sep)[-2]
                logging.info(path_component)
                logging.info(path_component.split('_')[1])
                flowid = int(path_component.split('_')[1])
                logging.info("calling updateState with workflow {} ".format(flowid))
                agent.updateState(flowid)
                i += 2
                continue

            if(sys.argv[i] == "-f" and i+1 < len(sys.argv)):
                logging.info("called agent with -f (finish workflow):"+sys.argv[i+1])
                task_id = agent.finishWorkflow(sys.argv[i+1])
                print(id)
                i += 2
                continue

            if(sys.argv[i] == "-r" and i+1 < len(sys.argv)):
                logging.info("called agent with -r (get report):"+sys.argv[i+1])
                task_id = agent.report(sys.argv[i+1])
                i += 2
                continue

            if(sys.argv[i] == "-h"):  #show help
                i += 1
                print("eventually, there will be some modicum of help in here...")
                continue

            if(sys.argv[i] == "-state"): #show state of tasks
                i += 1
                print("show state: running tasks, completed tasks, pending tasks")
                continue


            if(sys.argv[i] == "-a"):  #archive, cleans var, etc...
                i += 1
                continue

            print("wrong parameters? try: agent -h")
            logging.info(sys.argv[i])
            break

    except Exception as e:
        logging.exception(e)
        print("A nasty error occurred. Check the log for more details...")
        print("for your conveniency...:")
        print(e)
        print("--------")
        
        #print log last elements
        from collections import deque
        tail = deque(open(settings.agent_path+'/agent.log','r'), 20)
        for line in tail:
            print(line, end=" ")
    finally:
        if os.path.exists(settings.global_filelock_path):
            os.remove(settings.global_filelock_path)
        logging.info("finished agent run")

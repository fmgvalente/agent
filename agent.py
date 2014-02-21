
import sys
import subprocess
import glob
import logging
import shelve
import workflow
import settings


logging.basicConfig(filename='agent.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Agent(object):

    """Implements job monitoring"""
    def __init__(self, persistent_state):
        sys.path = [settings.modules_path] + sys.path
        sys.path = [settings.agent_path] + sys.path
        sys.path = [settings.workflows_path] + sys.path

        self.state = persistent_state
        self.init_persistent_state()

    def init_persistent_state(self):
        if(not 'id_counter' in self.state):
            self.state['id_counter'] = 0

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
        print(flow.id)

    def updateState(self, job_id):
        print("updating state")
        flow = workflow.from_id(job_id)
        flow.updateState()

    def cancelWorkflow():
        pass

    def signal_state_change():
        pass

    def id_increment_and_get(self):
        self.state['id_counter'] += 1
        return self.state['id_counter']


if __name__ == "__main__":
    logging.info("called agent with: "+repr(sys.argv))

    if (len(sys.argv)==0):
        import socket
        print(socket.gethostname())
        


    persistent_state = shelve.open(settings.persistent_state_path, writeback=True)

    agent = Agent(persistent_state)
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

            if(sys.argv[i] == "-u" and i+1 < len(sys.argv)):
                logging.info("called agent with -u (update state):"+sys.argv[i+1])
                agent.updateState(int(sys.argv[i+1]))
                i += 2
                continue

            logging.info("wrong parameters?")
            logging.info(sys.argv[i])
            break

    except Exception as e:
        logging.exception(e)
        print("A nasty error occurred. Check the log for more details...")
        print("...for your conveniency:")
        print(e)
        print("--------")

    persistent_state.close()

import os


#general configuration
agent_path = os.path.dirname(os.path.realpath(__file__))
modules_path = os.path.dirname(os.path.realpath(__file__))+"/modules"
workflows_path = os.path.dirname(os.path.realpath(__file__))+"/workflows"
persistent_state_path = os.path.dirname(os.path.realpath(__file__))+"/persistentstate"
execution_path = os.path.dirname(os.path.realpath(__file__))+"/var"
global_filelock_path = os.path.dirname(os.path.realpath(__file__))+"/agent_lock.lock"
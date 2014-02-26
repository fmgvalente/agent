import subprocess
import settings
import logging


def launch(output_dir):
    
    logging.info("launching feature_extraction to:"+output_dir)

    file = open(output_dir+"/launch.sh",'w')

    script = "#!/bin/sh\n"
    script += "#SBATCH --nodes=2\n"
    script += "#SBATCH --partition=gpu.test\n"
    #script += "srun ./mpisend\n"
    script += "srun hostname>{}/ff\n".format(output_dir)
    script += "touch {}\n".format(output_dir+"/_state_finished")
    script += "python ~/dev/agent/agent.py -ud {}".format(output_dir)


    file.write(script)
    file.close()

    subprocess.Popen(["sbatch", output_dir+"/launch.sh"])    
    #needs to get task id and that info




def collect(output_dir):
    print ("collect init from:"+output_dir)


if __name__ == "__main__":
    print("no test here for main...")

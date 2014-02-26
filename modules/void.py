import subprocess
import settings



def launch(output_dir):
    
    print("launching void to:"+output_dir)
    file = open(output_dir+"/launch.sh",'w')

    script = "#!/bin/sh\n"
    script += "#SBATCH --nodes=2\n"
    script += "#SBATCH --partition=gpu.test\n"
    script += "srun hostname>{}/ff\n".format(output_dir)
    script += "sleep 10\n"
    script += "touch {}\n".format(output_dir+"/_state_finished")
    script += "python {} -ud {}".format(settings.agent_path+"/agent.py", output_dir)

    file.write(script)
    file.close()

    subprocess.Popen(["sbatch", output_dir+"/launch.sh"])



def collect(output_dir):
    print ("collect init from:"+output_dir)


if __name__ == "__main__":
    print("no test here for main...")

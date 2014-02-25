import subprocess


def launch(output_dir):
    
    print("launching final to:"+output_dir)
    print("changing state")

    print("creating script file:{}".format(output_dir+"/launch.sh"))

    file = open(output_dir+"/launch.sh",'w')

    script = "#!/bin/sh\n"
    script += "#SBATCH --nodes=2\n"
    script += "#SBATCH --partition=gpu.test\n"
    #script += "srun ./mpisend\n"
    script += "touch {}\n".format(output_dir+"/_state_finished")

    file.write(script)
    file.close()

    print("launching script file")
    subprocess.call(["sh", output_dir+"/launch.sh"])

    print("end of task")



def collect(output_dir):
    print ("collect init from:"+output_dir)

if __name__ == "__main__":
    print("no test here for main...")
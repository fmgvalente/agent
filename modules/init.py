import subprocess


def launch(output_dir):
    
    print("launching init to:"+output_dir)
    print("creating script file:{}".format(output_dir+"/launch.sh"))

    file = open(output_dir+"/launch.sh",'w')

    script = "#!/bin/sh\n"
    script += "#SBATCH --nodes=2\n"
    script += "#SBATCH --partition=gpu.test\n"
    script += "srun ./mpisend\n"
    script += "exit 0\n"

    file.write(script)
    file.close()

    print("launching script file")
    subprocess.call(["sbatch",output_dir+"/launch.sh"])


    print("end of task")



def collect(output_dir):
    print ("collect init from:"+output_dir)


if __name__ == "__main__":
    print("no test here for main...")
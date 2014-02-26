import subprocess


def launch(output_dir):
    
    print("launching text_printer to:"+output_dir)

    file = open(output_dir+"/launch.sh",'w')

    script = "#!/bin/sh\n"
    script += "#SBATCH --nodes=2\n"
    script += "#SBATCH --partition=gpu.test\n"
    #script += "srun ./mpisend\n"
    script += "touch {}\n".format(output_dir+"/_state_finished")
    script += "python ~/dev/agent/agent.py -ud {}".format(output_dir)

    file.write(script)
    file.close()

    subprocess.Popen(["sh", output_dir+"/launch.sh"])


def collect(output_dir):
    print ("collect init from:"+output_dir)


if __name__ == "__main__":
    print("no test here for main...")
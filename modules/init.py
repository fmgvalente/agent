from .. import agent


def launch(output_dir):
    agent = agent.Agent()
    
    print("launching init to:"+output_dir)

    print("end of task")



def collect(output_dir):
    print ("collect init from:"+output_dir)


if __name__ == "__main__":
    launch("./")
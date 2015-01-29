_author__ = 'nick'

import getopt
import imp
import sys
import threading
import time
import yaml


class Agent(object):
    def __init__(self, mid, name, call, description, interval):
        self.mid = mid
        self.name = name
        self.call = call
        self.description = description
        self.interval = interval


def load_agents():
    agent_list = []
    agent_file = open("agents.yaml", "r")
    agent_docs = yaml.load_all(agent_file)

    for doc in agent_docs:
        a = Agent(doc['Id'], doc['Name'], doc['Call'], doc['Description'], doc['Interval'])
        agent_list.append(a)

    return agent_list


def load_arguments(agent_list):
    long_arguments = []

    for agent in agent_list:
        long_arguments.append(agent.mid+"=")

    return long_arguments


def parse_arguments(argv, long_arguments, agent_list):

    try:
        opts, args = getopt.getopt(argv, "hl", long_arguments)

    except getopt.GetoptError:
        print 'Invalid Usage'
        # print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            # print_help()
            print 'that is how you use it'
            sys.exit()
        elif opt == '-l':
            # print_agent_list()
            print "these are the agents"
            sys.exit()
        else:
            for agent in agent_list:
                if agent.mid == opt.replace('--', ''):
                    agent.interval = int(arg)

    return agent_list


def make_exec_lists(agent_list):

    run_list = {}
    iter_list = {}
    stream_list = {}
    idle_list = {}

    for agent in agent_list:
        # NOTE: revise that if statement
        if agent.interval < 0:  # first we check if it shall not run at all
            idle_list[agent.mid] = agent.interval
        elif agent.call == 'Streaming':  # then we check if it's a streaming call
            stream_list[agent.mid] = agent.interval
        elif agent.interval == 0:  # if none of the above conditions apply then it must be a request based call. run once
            run_list[agent.mid] = agent.interval
        else:  # or run continuously
            iter_list[agent.mid] = agent.interval
    return [run_list, iter_list, stream_list, idle_list]


def print_info(exec_list):
    for k in exec_list[0]:
        print k + " will run just once"
    for k in exec_list[1]:
        print k + " will run every " + str(exec_list[1][k]) + " minutes"
    for k in exec_list[2]:
        print k + " will stream for ever"
    for k in exec_list[3]:
        print k + " won't run"


def run_one(name, path):
    func = imp.load_source(name, path)
    t = threading.Thread(target=func.run, args=[])
    t.start()


def run_all(run_list):
    for agent in run_list:
        path = "request/" + agent + "/" + agent + ".py"
        run_one(agent, path)


def iterate_one(name, path, interval):
    func = imp.load_source(name, path)
    t = threading.Thread(target=func.iterate, args=[interval])
    t.setDaemon(True)
    t.start()


def iterate_all(iter_list):
    for agent in iter_list:
        path = "request/" + agent + "/" + agent + ".py"
        iterate_one(agent, path, iter_list[agent]*60)


def stream_one(name, path):
    func = imp.load_source(name, path)
    t = threading.Thread(target=func.fire, args=[])
    t.setDaemon(True)
    t.start()


def stream_all(stream_list):
    for agent in stream_list:
        path = "streaming/" + agent + "/" + agent + ".py"
        stream_one(agent, path)




def main(argv):

    agent_list = load_agents()  # load all available retrieval agents with defaults
    long_arguments = load_arguments(agent_list) #
    agent_list = parse_arguments(argv, long_arguments, agent_list)
    exec_list = make_exec_lists(agent_list)
    print_info(exec_list)
    run_all(exec_list[0])
    iterate_all(exec_list[1])
    stream_all(exec_list[2])

    if len(exec_list[1]) != 0 or len(exec_list[2]) != 0:
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1:])


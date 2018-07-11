import portpicker
import subprocess
import sys
from datetime import datetime

from config_generator import ConfigGenerator
from summaries_reader import SummariesReader

class TrainRunner(object):
    def __init__(self, env_name):
        self.env_name = env_name
        self.conf_gen = ConfigGenerator()

    def f(self, params):
        '''
        Function to optimize
        Runs a training process and wait for its termination
        '''
        run_id = self.env_name + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")

        conf_path = self.conf_gen.generate(self.env_name, params, run_id)
        proc = self.start_train_process(conf_path, run_id)
        for line in iter(proc.stdout.readline, b''):
            print('[{0}] {1}'.format(proc.pid, line.decode('utf-8')), end='')
        proc.wait()

        reward = SummariesReader(run_id).get_scalar('Info/cumulative_reward')[-1].value

        return reward

    # # x^2 + y^3 + 5
    # def f(self, params):
    #     return params[0][0]**2 + params[0][1] **3 + 5

    def start_train_process(self, conf_path, run_id):
        unused_port = portpicker.pick_unused_port()
        proc = subprocess.Popen(['python', 'learn.py', self.env_name, '--train', '--worker-id=' + str(unused_port), '--trainer-config-path=' + str(conf_path), '--run-id=' + run_id],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return proc

if __name__ == '__main__':
    train_runner = TrainRunner('test123')
    reward = train_runner.f([[1,1]])
    print(reward)

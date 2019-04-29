from __future__ import absolute_import
from __future__ import print_function
try: xrange
except: xrange = range
import subprocess
import re
import time

def main(num_trials, test, first_test, last_test):
    result_file = 'results/{}.csv'.format(test)
    error_file = 'errors/{}.txt'.format(test)
    log_file = 'logs/{}.txt'.format(test)
    input_dir = 'input_{}'.format(test)
    with open(result_file, 'w') as f: pass
    with open(error_file, 'w') as f: pass
    with open('{}/test.sk'.format(input_dir)) as f: text = f.read()
    log = open(log_file, 'w')
    if last_test == 0: last_test = int(re.findall(r't[0-9]+', text)[-1][1:])
    for i in xrange(first_test + 1 if first_test == -1 else first_test, last_test+1):
        print('Running test {}'.format(i))
        times = []
        for j in xrange(num_trials):
            cmd = ['sketch', '--fe-def', 'TID={}'.format(i), '--fe-inc', input_dir, '{}/main.sk'.format(input_dir)]
            log.write('test: {}, trial: {}, cmd: {}\n'.format(i, j, ' '.join(cmd)))
            log.flush()
            try:
                t = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                start = t.rfind('Total time = ') + len('Total time = ')
                times.append(float(t[start:t.find('\n', start)]))
                time.sleep(1)
            except:
                print('ERROR: {}'.format(' '.join(cmd)))
                with open(error_file, 'a') as f: f.write('{}\n'.format(' '.join(cmd)))
                times.extend([0.0]*num_trials)
                break
        if first_test != -1: print('Test: {}, times: {}'.format(i, times))
        with open(result_file, 'a') as f:
            [f.write('{:.2f}\t'.format(n)) for n in times]
            f.write('\n')
    sort_results(test)

def sort_results(test):
    result_file = 'results/{}.csv'.format(test)
    sorted_result_file = 'results/{}_s.csv'.format(test)
    with open(result_file,'r') as fd:
        lines = fd.readlines()
    # do it all on one line! (split line, convert to float, sort)
    res = map(lambda l: sorted(map(float, l.strip('\n\t').split('\t') if l.split('\t') != [''] else [0])), lines)
    with open(sorted_result_file, 'w') as fd:
        for r in res: fd.write('{}\n'.format('\t'.join(map(str,r))))
    
if __name__ == '__main__':
    from optparse import OptionParser
    jskparser = OptionParser(usage="%prog [options]*")
    jskparser.add_option('-i', action='store_true', dest='impl', default=False,
                      help='Execute implementation tests.')
    jskparser.add_option('--an', action='store_true', dest='adt_n', default=False,
                      help='Execute non-deterministic adt tests.')
    jskparser.add_option('--ad', action='store_true', dest='adt_d', default=False,
                      help='Execute deterministic adt tests.')
    jskparser.add_option('-o', action='store_true', dest='obj', default=False,
                      help='Execute Object tests.')
    jskparser.add_option('-n', action='store', type='int', dest='trials', default=1,
                      help='Number of trials to run.')
    jskparser.add_option('-f', action='store', type='int', dest='first_test', default=-1,
                      help='First test to run.')
    jskparser.add_option('-l', action='store', type='int', dest='last_test', default=0,
                      help='Last test to run.')
    (options, args) = jskparser.parse_args()
    print('Number of trials: {}'.format(options.trials))
    if options.impl:
        print('Testing implementation')
        main(options.trials, 'impl', options.first_test, options.last_test)
        print()
    if options.adt_n:
        print('Testing non-deterministic adt')
        main(options.trials, 'adt_n', options.first_test, options.last_test)
        print()
    if options.adt_d:
        print('Testing deterministic adt')
        main(options.trials, 'adt_d', options.first_test, options.last_test)
        print()
    if options.obj:
        print('Testing Object')
        main(options.trials, 'Object', options.first_test, options.last_test)
        print()
    if (not options.impl) and (not options.adt_n) and (not options.adt_d) and (not options.obj):
        print('Testing implementation')
        main(options.trials, 'impl', options.first_test, options.last_test)
        print('Testing non-deterministic adt')
        main(options.trials, 'adt_n', options.first_test, options.last_test)
        print('Testing deterministic adt')
        main(options.trials, 'adt_d', options.first_test, options.last_test)
        print('Testing Object')
        main(options.trials, 'Object', options.first_test, options.last_test)

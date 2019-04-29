from __future__ import absolute_import
from __future__ import print_function
import subprocess
import re
import math
import time

def main(num_trials, test):
    result_file = 'results/{}.csv'.format(test)
    error_file = 'errors/{}.txt'.format(test)
    log_file = 'logs/{}.txt'.format(test)
    input_dir = 'input_{}'.format(test)
    with open(result_file, 'w') as f: pass
    with open(error_file, 'w') as f: pass
    with open('{}/test.sk'.format(input_dir)) as f: text = f.read()
    log = open(log_file, 'w')
    num_tests=int(re.findall(r't[0-9]+', text)[-1][1:]) + 1
    for i in range(num_tests):
        print('Running test {}'.format(i))
        times = []
        for j in range(num_trials):
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
        with open(result_file, 'a') as f:
            [f.write('{:.2f}\t'.format(n)) for n in times]
            f.write('\n')
    combine()

def combine():
    def median(nums):
        nums.sort()
        mid = int(len(nums) / 2.0)
        if len(nums) % 2 == 0: return (nums[mid-1]+nums[mid])/2.0
        else: return nums[int(math.floor(mid))]
    
    with open('results/impl.csv','r') as impl_fd:
        impl_txt = [v.strip('\n\t') for v in impl_fd.readlines()]
    with open('results/adt.csv','r') as adt_fd:
        adt_txt = [v.strip('\n\t') for v in adt_fd.readlines()]
    with open('results/Object.csv','r') as obj_fd:
        Object_txt = [v.strip('\n\t') for v in obj_fd.readlines()]
    
    impl_fd = open('results/impl_s.csv','w')
    adt_fd = open('results/adt_s.csv','w')
    obj_fd = open('results/Object_s.csv','w')
    vals = []
    for i,a,o in zip(impl_txt, adt_txt, Object_txt):
        strs_i = i.split('\t') if i.split('\t') != [''] else [0]
        strs_a = a.split('\t') if a.split('\t') != [''] else [0]
        strs_o = o.split('\t') if o.split('\t') != [''] else [0]

        mi = median([float(s) for s in strs_i])
        ma = median([float(s) for s in strs_a])
        mo = median([float(s) for s in strs_o])
        vals.append((mi, ma, mo))

        # rewrite these in sorted order b/c Numbers on OS X is a POS
        impl_fd.write('{}\n'.format('\t'.join(map(str,sorted(map(float, strs_i))))))
        adt_fd.write('{}\n'.format('\t'.join(map(str,(sorted(map(float, strs_a)))))))
        obj_fd.write('{}\n'.format('\t'.join(map(str,(sorted(map(float, strs_o)))))))

    with open('results/all.csv', 'w') as f:
        for v in vals:
            f.write('{}\t{}\t{}\n'.format(v[0], v[1], v[2]))

if __name__ == '__main__':
    from optparse import OptionParser
    jskparser = OptionParser(usage="%prog [options]*")
    jskparser.add_option('-i', action='store_true', dest='impl', default=False,
                      help='Execute implementation tests.')
    jskparser.add_option('-a', action='store_true', dest='adt', default=False,
                      help='Execute adt tests.')
    jskparser.add_option('-o', action='store_true', dest='obj', default=False,
                      help='Execute Object tests.')
    jskparser.add_option('-n', action='store', type='int', dest='trials', default=1,
                      help='Number of trials to run.')
    (options, args) = jskparser.parse_args()
    print('Number of trials: {}'.format(options.trials))
    if options.impl:
        print('Testing implementation')
        main(options.trials, 'impl')
        print()
    if options.adt:
        print('Testing adt')
        main(options.trials, 'adt')
        print()
    if options.obj:
        print('Testing Object')
        main(options.trials, 'Object')
        print()
    if (not options.impl) and (not options.adt) and (not options.obj):
        print('Testing implementation')
        main(options.trials, 'impl')
        print('Testing adt')
        main(options.trials, 'adt')
        print('Testing Object')
        main(options.trials, 'Object')

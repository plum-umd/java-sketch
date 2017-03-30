import subprocess
import re
import math

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
        print 'Running test {}'.format(i)
        times = []
        for j in range(num_trials):
            cmd = ['sketch', '--fe-def', 'TID={}'.format(i), '--fe-inc', input_dir, '{}/main.sk'.format(input_dir)]
            log.write('test: {}, trial: {}, cmd: {}\n'.format(i, j, ' '.join(cmd)))
            log.flush()
            try:
                t = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                start = t.rfind('Total time = ') + len('Total time = ')
                times.append(float(t[start:t.find('\n', start)]))
            except:
                print 'ERROR: {}'.format(' '.join(cmd))
                with open(error_file, 'a') as f: f.write('{}\n'.format(' '.join(cmd)))
                times.extend([0.0]*num_trials)
                break
        with open(result_file, 'a') as f:
            [f.write('{:.2f}\t'.format(n)) for n in times]
            f.write('\n')

def combine():
    def median(nums):
        nums.sort()
        mid = int(len(nums) / 2.0)
        if len(nums) % 2 == 0: return (nums[mid-1]+nums[mid])/2.0
        else: return nums[int(math.floor(mid))]
    
    with open('results/impl.csv','r') as f: impl_txt = map(lambda v: v.strip('\n\t'), f.readlines())
    with open('results/adt.csv','r') as f: adt_txt = map(lambda v: v.strip('\n\t'), f.readlines())
    with open('results/Object.csv','r') as f: Object_txt = map(lambda v: v.strip('\n\t'), f.readlines())
    
    vals = []
    for i,a,o in zip(impl_txt, adt_txt, Object_txt):
        strs_i = i.split('\t') if i.split('\t') != [''] else [0]
        strs_a = a.split('\t') if a.split('\t') != [''] else [0]
        strs_o = o.split('\t') if o.split('\t') != [''] else [0]
        mi = median(map(float, strs_i))
        ma = median(map(float, strs_a))
        mo = median(map(float, strs_o))
        vals.append((mi, ma, mo))
    
    with open('results/all.csv', 'w') as f:
        map(lambda v: f.write('{}\t{}\t{}\n'.format(v[0], v[1], v[2])), vals)
    
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options]*")
    parser.add_option('-i', action='store_true', dest='impl', default=False,
                      help='Execute implementation tests.')
    parser.add_option('-a', action='store_true', dest='adt', default=False,
                      help='Execute adt tests.')
    parser.add_option('-o', action='store_true', dest='obj', default=False,
                      help='Execute Object tests.')
    parser.add_option('-n', action='store', type='int', dest='trials', default=1,
                      help='Number of trials to run.')
    (options, args) = parser.parse_args()
    print 'Number of trials: {}'.format(options.trials)
    if options.impl:
        print 'Testing implementation'
        main(options.trials, 'impl')
        print
    if options.adt:
        print 'Testing adt'
        main(options.trials, 'adt')
        print
    if options.obj:
        print 'Testing Object'
        main(options.trials, 'Object')
        print
    if (not options.impl) and (not options.adt) and (not options.obj):
        print 'Testing implementation'
        main(options.trials, 'impl')
        print 'Testing adt'
        main(options.trials, 'adt')
        print 'Testing Object'
        main(options.trials, 'Object')
        combine()

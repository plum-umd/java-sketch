import subprocess, sys

NUM_TESTS=9
NUM_TRIALS=int(sys.argv[1])

with open('results_impl.csv', 'w') as f: pass
for i in range(NUM_TESTS):
    times = []
    flag = 'TID={}'.format(i)
    for j in range(NUM_TRIALS):
        print 'test {}, trial {}'.format(i,j)
        cmd = ['sketch', '--fe-inc', 'input_impl/', 
               'input_impl/main.sk', '--fe-def', flag]

        print 'cmd:', ' '.join(cmd)
        t = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        start = t.rfind('Total time = ') + len('Total time = ')
        times.append(float(t[start:t.find('\n', start)]))
    with open('results_impl.csv', 'a') as f:
        [f.write('{:.2f}\t'.format(n)) for n in times]
        f.write('\n')



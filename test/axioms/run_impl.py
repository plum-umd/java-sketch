import subprocess
import sys
import re

with open('input_impl/test.sk') as f: test = f.read()
NUM_TESTS=int(re.findall(r't[0-9]+', test)[-1][1:])
NUM_TRIALS=int(sys.argv[1])

with open('results_impl.csv', 'w') as f: pass
with open('errors_impl.txt', 'w') as f: pass

for i in range(NUM_TESTS):
    times = []
    for j in range(NUM_TRIALS):
        cmd = ['sketch', '--fe-def', 'TID={}'.format(i), '--fe-inc', 'input_impl/', 'input_impl/main.sk']
        print 'test: {}, trial: {}, cmd: {}'.format(i, j, ' '.join(cmd))
        try:
            t = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            start = t.rfind('Total time = ') + len('Total time = ')
            times.append(float(t[start:t.find('\n', start)]))
        except:
            with open('errors_impl.txt', 'a') as f: f.write('{}\n'.format(' '.join(cmd)))
            break
    with open('results_impl.csv', 'a') as f:
        [f.write('{:.2f}\t'.format(n)) for n in times]
        f.write('\n')

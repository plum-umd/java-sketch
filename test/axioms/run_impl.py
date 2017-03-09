import subprocess

NUM_TESTS=subprocess.check_output(['find', 'input_impl', '-name', 'm[0-9].sk']).count('\n')
NUM_TRIALS=2

with open('results.csv', 'w') as f: pass
for i in range(NUM_TESTS):
    times = []
    for j in range(NUM_TRIALS):
        nm = 'input_impl/m{}.sk'.format(i)
        t = subprocess.check_output(['time', 'sketch', '--fe-inc', 'input_impl/', nm],
                                    stderr=subprocess.STDOUT)
        start = t.rfind('\n', t.rfind('='), t.rfind('user'))
        times.append(float(t[start+1:t.find('user', start)]))
    times.append(sum(times)/len(times))
    with open('results.csv', 'a') as f:
        [f.write('{:.2f}\t'.format(n)) for n in times]
        f.write('\n')



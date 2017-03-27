import math

def median(nums):
    nums.sort()
    mid = int(len(nums) / 2.0)
    if len(nums) % 2 == 0: return (nums[mid-1]+nums[mid])/2.0
    else: return nums[int(math.floor(mid))]

with open('results_impl.csv','r') as f: impl_txt = map(lambda v: v.strip('\n\t'), f.readlines())
with open('results_adt.csv','r') as f: adt_txt = map(lambda v: v.strip('\n\t'), f.readlines())

vals = []
for i,j in zip(impl_txt, adt_txt):
    strs_i = i.split('\t')
    strs_j = j.split('\t')
    mi = median(map(float, strs_i))
    mj = median(map(float, strs_j))
    vals.append((mi,mj))

with open('results.csv', 'w') as f:
    map(lambda v: f.write('{}\t{}\n'.format(v[0], v[1])), vals)

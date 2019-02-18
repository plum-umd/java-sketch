from __future__ import absolute_import
from __future__ import print_function
import sys
import re

FILE_NAME=sys.argv[1]
print(FILE_NAME)
FILE_RENAME=FILE_NAME[:FILE_NAME.rfind('.')]+'.csv'
print(FILE_RENAME)

with open(FILE_NAME, 'r') as f: text = f.read()
text = re.sub(r'\n', '', text)
text = re.sub(r'Number of trials: 15Testing .+?Running test 8Test: 8, times: \[', '', text)
text = re.sub('\]', '\n', text)
text = re.sub(', ', '\t', text)
print(text)
with open(FILE_RENAME, 'w') as f: f.write(text)

import sys
import re
import collections

WORD_RE = re.compile('\w+')

index = collections.defaultdict(list)
print(index.default_factory())
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp):
        for match in WORD_RE.finditer(line):
            word = match.group()
            col_no = match.start() + 1
            location = (line_no, col_no)
            index[word].append(location)

for word in sorted(index, key = str.upper):
    print(word, index[word])


            


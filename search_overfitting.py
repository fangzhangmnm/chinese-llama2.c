text='洗脸'


# search ./data/TinyStories_all_data/*.jsonl to look for duplicity


from glob import glob
import re
from tqdm.auto import tqdm

print('searching for: ', text)

found=False
for filename in tqdm(glob('./data/TinyStories_all_data/*.jsonl')):
    with open(filename, 'r',encoding='utf-8') as f:
        for line in f:
            if re.search(text, line):
                print('duplicate found in: ', filename, 'line: ', line)
                found=True

if not found:
    print('no duplicate found')

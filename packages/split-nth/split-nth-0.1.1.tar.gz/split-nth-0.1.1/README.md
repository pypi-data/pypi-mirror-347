# split-nth

A small utility to split a string at the N-th occurrence of a specific word.

## Installation

```bash
pip install split_nth


##Usage
from split_nth import split_on_word

s = "cast (int as dec) as abcas"
print(split_on_word(s, word="as", occ=2))
# Output: ['cast (int as dec)', 'abcas']



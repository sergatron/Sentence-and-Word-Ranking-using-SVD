import os
import sys

# get arguments for URL target and output file name
url_target = sys.argv[1]
outfile = sys.argv[2]

# create text file
os.system(f"python get_text.py {url_target} {outfile}")


# Word Rank
os.system(f"python word_rank.py articles/{outfile}.txt")


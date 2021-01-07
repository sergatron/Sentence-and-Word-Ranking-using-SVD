# Word/Sentence Ranking using SVD

Extract text from HTML using the file `get_text.py` by providing it a URL. 
It will output a text file into the `articles/` directory which can be accessed by `word_rank.py`

# Usage 

### Extract Text
Extract text from a given URL and save to a file. 
```buildoutcfg
python get_text.py <Target_URL> <output_filename>
```

Executing the above will output a new text file to `articles/output_filename.txt`. Note, extention should not be provided. By default, the provided file name will be saved with `.txt` extension. 

### Word Rank
```buildoutcfg
python word_rank.py <filepath>
```

The `filepath` represents the text file to perform SVD ranking. This file should be located in the `articles/` directory.
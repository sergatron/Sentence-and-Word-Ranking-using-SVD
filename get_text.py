import sys
from bs4 import BeautifulSoup as bs
import requests


# make request to target URL

# url = "https://finance.yahoo.com/news/3-chip-stocks-room-grow-204840835.html"
# url = sys.argv[1]

def make_request(url_target):
    """
    Send request to URL. If connection is not established, then
    an Exception is raised.

    Returns
    -------
    req:
        requests.models.Response

    """
    req = requests.get(url_target)

    if req.status_code != 200:
        raise Exception("Web request failed!")

    return req


def get_soup(req):
    """
    Parses HTML and return BeautifulSoup object

    Params
    -------
    req : requests.models.Response


    Returns
    -------
    BeautifulSoup object
    """

    # parse HTML
    return bs(req.text, 'html.parser')


def extract_paragraphs(bsoup, print_count=False):
    """
    Takes in BeautifulSoup object and extracts paragraphs.
    Optionally, prints out the number of paragraphs.

    Params
    -------
    bsoup : BeautifulSoup object

    Returns
    -------
    full_text:
        str; all paragraphs concatenated

    """
    # find all paragraph tags and put together into one article
    full_text = ''
    par_count = 0

    # iterate over found paragraphs and combine
    for par in bsoup.find_all('p'):
        full_text += par.text
        par_count += 1

    if print_count:
        print('Num of Paragraphs:', par_count)

    return full_text


def preview_text(text, n=100):
    """
    Preview the first `n` chars of text.

    Params
    -------
    text : str
    n : int

    Returns
    -------
    NoneType
    """
    # preview text
    print('\n\n')
    print(text[:n])
    print('-'*100)



def write_file(filename, content):
    """Save to a text file. Extension does not need to be provided."""

    # write content to file
    save_path = f"articles/{filename}.txt"

    with open(save_path, 'w', encoding='utf-8') as new_f:
        print(f'Writing to... \n {save_path} ... \n')
        new_f.write(content)
        print('Finished!')



if __name__ == '__main__':


    # get URL from user, and name of output file
    url = sys.argv[1]
    outfile = sys.argv[2]

    # create BeautifulSoup object
    bs = get_soup(make_request(url))

    # get paragraphs from Soup
    text = extract_paragraphs(bs)

    preview_text(text)

    # save output to files
    write_file(outfile, text)


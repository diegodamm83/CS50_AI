import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """ 
    # Define a dictionary to store the probabilities
    probabilities = {}

    # Links within the page i can reach with damping factor probability
    page_links = corpus[page]

    # Links I can go to from any page with equal probability
    all_pages = []
    for pages in corpus:
        all_pages.append(pages)
        # Iniciamos diccionario de probabilidades
        probabilities[pages] = 0

   # Probability of going to a page from the page i am in
    for page in page_links:
        probabilities[page] = damping_factor * (1/len(page_links))
        
    # Probability of going to a page randomly
    for page in all_pages:
        probabilities[page] += (1-damping_factor) * (1/len(all_pages))
    
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())

    # Store pages and their sample probabilites and initialize every page's probability 0
    createdPages = {}
    for page in pages:
        createdPages[page] = 0

    # choose a first page at random
    first_page = random.choice(pages)

    # Set its probability to 1/n because it is one out of n samples
    createdPages[first_page] = 1/n

    # get probability of going to another page from current page based on transition model
    current_probabilities = transition_model(corpus, first_page, damping_factor)

    # create the rest of samples
    for i in range(0, n-1):
        new_page = random.choices(list(current_probabilities.keys()), list(current_probabilities.values()), k=1)
        createdPages[new_page[0]] += 1/n
        current_probabilities = transition_model(corpus, new_page[0], damping_factor)
    
    return createdPages




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    threshold = 0.0005
    N = len(corpus)
    
    for key in corpus:
        ranks[key] = 1 / N
    for key in corpus:
        ranks[key] = 1 / N

    while True:
        count = 0
        for key in corpus:
            new = (1 - damping_factor) / N
            sigma = 0
            for page in corpus:
                if key in corpus[page]:
                    num_links = len(corpus[page])
                    sigma = sigma + ranks[page] / num_links
            sigma = damping_factor * sigma
            new += sigma
            if abs(ranks[key] - new) < threshold:
                count += 1
            ranks[key] = new 
        if count == N:
            break
    return ranks



if __name__ == "__main__":
    main()

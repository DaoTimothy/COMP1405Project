Partners:
Brandon Le
Timothy Dao

Instructions for running in command line:

To run the crawl at "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html": (replace the link with your own)
python -c "import crawler; crawler.crawl(\"http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html\")"

To search and print the results for the query "coconut apple" with boost = True: (you can change the search query and boost to whatever you'd like)
python -c "import search; print(search.search(\"coconut apple\", True))"
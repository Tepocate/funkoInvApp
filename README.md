# FunkoInvApp

This is a personal project that will allow the user to go to one place for all there Funko needs. The interface will have an Image of the product, name, price, promotions, and link that will allow you to add the product straight to your cart and pay from the website.

## Installation of Dependencies

to install the dependencies all you need to do it have pipenv installed and do the follwoing commands in the same directory the Pipfile and Pipfile.lock files are in:

```bash
$ pipenv install
```

## Running the App so far

Once the dependencies from the Pipfile and Pipfile.lock are installed navigate to the directory where you will find web_scraping.py. It should be in FunkoInvApp/code/web_scraping.py from here you have a couple of options on running the python file.

```bash
$ pipenv run python web_scraping.py
```

OR

```bash
$ pipenv shell # This will initiate a virtual enviroment
$ python web_scraping.py
```

If you want to learn more about pipenv [Here](https://pipenv-fork.readthedocs.io/en/latest/basics.html)

## Roadmap

I still need to web scrape a few more site and figure out what tools I will use to build the actual UI.

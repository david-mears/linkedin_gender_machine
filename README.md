# LinkedIn Gender Machine

A command-line-interface app that guesses at the gender-proportions of companies who have LinkedIn profiles. Caveat: you can't tell someone's gender from their name, for a variety of reasons. So take the data with a pinch of salt.

## Installation

Create and activate the virtual environment. Then:

```
$ pip install -r requirements.txt
```

Create a .env file in the root directory, and put in LINKEDIN_USERNAME=<your_username> and LINKEDIN_PASSWORD=<your_password>.

## Uses

```
$ python script.py <comapny_url>
```
e.g.

```
$ python script.py https://www.linkedin.com/company/tails-com
```
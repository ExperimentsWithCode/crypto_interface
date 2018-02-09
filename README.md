# Crypto Interface

## Goal:
* Track mentions on 4Chan, Reddit Comments, Reddit Posts
* a lot of other cool shit
* Add more base pairs

# Currently:
* Can hardcode portfolio pairs and view current USD value from converting through ETH.
* Can view load currency info
* Can load ETH price

* Can update current 4Chan threads. This will not overwrite previously stored data, and will not double counts

* Can display current 4Chan mention counts.

## Config file
You must set up a config.py file and store it in the home directory of the project. This file is meant to store all locally relevant credentials. This file should include the following:

```
REDDIT_SECRET = "____"
REDDIT_API    = "____"
DB_NAME       = "____"
DB_USER       = "____"
```
## To run
```
  $ python main.py
```
OR
```
  from main import Main
  m = Main()
  m.run()
```

## Basic Interface:
```
Select what you would like to do
	Enter `a` to `Crypto Interface`
	Enter `b` to `4Chan Interface`
	Enter `exit` to `exit`

Select: b

...

Select what you would like to do
	Enter `a` to `Update Datastore`
	Enter `b` to `Display Counts`
	Enter `main` to `return to main`
	Enter `exit` to `exit`
Select: b

	Display Counts
		ADA: 3 mentions
		AM: 10 mentions
		AMP: 2 mentions
		ANT: 4 mentions
		ARK: 9 mentions
		BAT: 20 mentions
		BLOCK: 1 mentions
		BNT: 7 mentions
		BTC: 75 mentions
		CLUB: 1 mentions
		CRYPT: 1 mentions
		DASH: 1 mentions
		DGB: 1 mentions
		DNT: 1 mentions
		DOGE: 3 mentions

  ...
```


## Dependencies
* python

### Libraries
  * json
  * requests
  * collections
  * basc_py4chan


## To DO:
* [ ] Separate Currencies from base pairs
* [ ] Add value options between base currencies
* [ ] I/O for portfolio
* [ ] proper DB for mentions history
* [x] Add tracking for Reddit
*

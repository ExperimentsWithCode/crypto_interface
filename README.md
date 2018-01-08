# Crypto Interface

# Goal:
* Track mentions on 4Chan, Reddit Comments, Reddit Posts
* a lot of other cool shit
* Add more base pairs

# Currently:
* Can hardcode portfolio pairs and view current USD value from converting through ETH.
* Can view load currency info
* Can load ETH price

* Can update current 4Chan threads. This will not overwrite previously stored data, and will not double counts

* Can display current 4Chan mention counts.


# To run

  $ python main.py

OR

  from main import Main
  m = Main()
  m.run()


# Basic Interface:

Select what you would like to do
	Enter `a` to `Crypto Interface`
	Enter `b` to `4Chan Interface`
	Enter `exit` to `exit`


# Dependencies
* python

## Libraries
  * json
  * requests
  * collections
  * basc_py4chan

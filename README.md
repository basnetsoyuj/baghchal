# baghchal

[![Build Status](https://travis-ci.org/basnetsoyuj/baghchal.svg?branch=master)](https://travis-ci.org/basnetsoyuj/baghchal) [![Documentation Status](https://readthedocs.org/projects/baghchal/badge/?version=latest)](https://baghchal.readthedocs.io/en/latest/?badge=latest) [![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

baghchal is a pure Python Bagh Chal library that supports game import, move generation, move validation and board image rendering. It also comes with a simple engine based on minimax algorithm and alpha-beta pruning.


 
## Installation
baghchal runs on python 3 . You can now install it directly from PyPI via pip:

```
	pip install baghchal
```

System requirements are [numpy](https://pypi.org/project/numpy/) and  [Pillow](https://pypi.org/project/Pillow/).

## Source Code
The source code can be found [here](https://github.com/basnetsoyuj/baghchal).

## Documentation 
The baghchal package has 3 sub-modules:
* baghchal.**env** ( Consists of all classes and functions defining the game environment )
	* baghchal.env.**Board** (Board class representing BaghChal board)
	* baghchal.env.**Bagh** (Bagh class representing Bagh Player)
	* baghchal.env.**Goat** (Goat class representing Goat Player)


* baghchal.**lookup_table** ( Lookup values for baghchal.env )

* baghchal.**engine** ( Simple engine based on minimax algorithm and alpha-beta pruning )
	* baghchal.engine.**Engine**

More detailed documentation for baghchal library is available [here](https://baghchal.readthedocs.io/en/latest/).

## License
baghchal is licensed under MIT License . Check out [LICENSE.txt](https://github.com/basnetsoyuj/baghchal/blob/master/LICENSE.txt) for the full text.
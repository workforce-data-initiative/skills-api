#REBUILDD API

This project is entirely based on [this project](https://github.com/dssg/labor) and it's an attempt to decouple the API from the rest of the project. 

The objective is to build an API that scales easily.

All credit goes to the labor team. Labor!

##Main changes from the original `app` and `rebuildd` folders

* The Flask now includes a sript to be deployed on gunicorn
* Many HTML files were deleted since this project is going to be API only
* rebuildd is now a Python package so it's easy to import (just do `python setup.py`)

## License
MIT license, see [LICENSE.txt](LICENSE.txt)

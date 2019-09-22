# OptiTrek Gateway

A web server that serves offline OptiTrack data, that has been exported as CSV,
via a websocket connection.

## Install

`pipenv install`

(This doesn't currently work because pipenv doesn't play well with pandas or
numpy. Instead, `pipenv shell` and then `pip install` each of the packages
listed in `Pipfile`.)

## Create CSV Files

Place the OptiTrack CSV files in `./data` (or create a symbolic link from
`/.data` to their location).

`pipenv run create-csv`

This creates `*.json` files in `./build`.

## Server data

`pipenv run server`

This serves data from the first `*.json` file in `./build`.

## References

* [OptiTrack CSV](https://v21.wiki.optitrack.com/index.php?title=Data_Export:_CSV)
* [websockets](https://websockets.readthedocs.io/en/stable/)

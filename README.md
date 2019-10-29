# OptiTrek Gateway

A web server that serves offline OptiTrack data, that has been exported as CSV,
via a websocket connection.

## Install

`pipenv install`

## Create CSV Files

`pipenv run create-csv FILE_OR_DIR...`

This creates `*.json` files in `./build`, from the *.csv files at
`FILE_OR_DIRNAME`.

`pipenv run create-csv FILE_OR_DIR...` prints the bone names.

## Server data

`pipenv run server`

This serves data from the first `*.json` file in `./build`.

## References

* [OptiTrack CSV](https://v21.wiki.optitrack.com/index.php?title=Data_Export:_CSV)
* [websockets](https://websockets.readthedocs.io/en/stable/)

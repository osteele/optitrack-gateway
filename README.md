# OptiTrack Gateway

A web server that serves offline OptiTrack data, that has been exported as CSV,
via a websocket connection.

It is meant to be used in conjunction with the web client in
<https://github.com/osteele/p5pose-optitrack>.

## Install

1. Verify that will python3 and pipenv are installed:

   ```sh
    python3 --version
    pipenv --version
    ```

    The first command should print `Python 3.7.4` or greater.

    The second command should print something like `pipenv, version 2018.11.26`.
    It doesn't matter exactly what it prints, it just shouldn't error.

2. If python3 and pipenv are not installed, install them. On macOS:

   1. Install [homebrew](https://brew.sh)
   2. Run the terminal commands:

      ```sh
      brew install python pipenv
      ```

   On other operating systems, follow the instructions
   [here](https://pipenv.kennethreitz.org/en/latest/) to install pipenv.

3. Clone this repository
4. Inside the cloned directory, run this command:

   ```sh
   pipenv install
   ```

## Create CSV Files

You will need an OptiTrack *.csv file.

Use the following command to convert this file to JSON:

`pipenv run create-csv FILE_OR_DIR...`

This creates `*.json` files in `./build`, from the *.csv files at
`FILE_OR_DIRNAME`.

If `FILE_OR_DIRNAME` is a path, it converts a single file.

If `FILE_OR_DIRNAME` is a directory, all *.csv files *directly* inside that
directory (but not files inside directories in that directory) are converted.

`pipenv run print-bones FILE_OR_DIR...`

Prints the bone names.

## Run the Server

`pipenv run server [JSON_PATH]`

This serves data from `JSON_PATH`. If this file is absent, the first `*.json`
file in `./build` is used.

## References

* [OptiTrack CSV](https://v21.wiki.optitrack.com/index.php?title=Data_Export:_CSV)
* [websockets](https://websockets.readthedocs.io/en/stable/)

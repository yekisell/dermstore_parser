# Dermstore parser

This package allows you to parse data from dermstore.com (just a single page).
## Usage
1. Clone this repo to your local machine
2. Install all packages from requirements.txt
```sh
pip install -r requirements.txt
```
3. Run parser with following command:
```sh
python parser.py -u <url of parsing page>
```
You can configure additional options:
```sh
-a (bool) — determines whether to append object to existing csv file (True) or make a single csv file with it (False)
-s (str) — path where the object will be saved
```

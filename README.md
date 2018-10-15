# christies-data-extraction
Web data extraction and comparison from a Christie's art sale.

## Introduction
The goal is to extract data from two Christie's art auction (Nov. 2017 and Mar. 2018) and compare the avg selling price for similar lots by the same artist. The definition of similar is based on the lot's dimensions, where they are similar if within some +/- threshold. The main program's output is a CSV file containing the comparisons for each artist's groupings, with a user specifed similarity threshold.

## How-To
*Requires Python 3.6*

The first step after downloading the repository is to install all required dependencies:
```
pip install -r requirements.txt
```
Then, we need to extract the data from the Christie's website. The `data_extraction` script requires configuration variables from a .env file (which for security reasons has been excluded from the repo). To obtain the proper .env file, please email me at [scottyargeau@gmail.com](mailto:scottyargeau@gmail.com). Once you have the .env file, run:
```
python data_extraction.py
```
Finally, the main program can be ran from some user specified similarity threshold X as follows:
```
python main.py X
```
You should now see two raw data source files `nov_2017_data.csv` and `mar_2018_data.csv` and one main report file `report.csv`.

## Considerations & Future Tasks
For easy HTML DOM manipulation, beautifulsoup 4 was used. This allows us to take HTML data from the HTTP request response and extract strings from specific tags that we desire. For data processing and manipulation after extraction, we use pandas to organize data in a tabular manner and eventually output the report as a CSV.

The source URLs are contained in a separate .env file (as mentioned above) as to avoid misuse of request data from the server. This also represents how I expect confidential info to be kept away from git repositories. The package python-dotenv is used to access variables within the .env file.

Example unit tests are shown in `test.py`. These can be ran by:
```
python -m test
```
For a production service, I would expect all custom functionality to be unit tested. Due to time constraints, I chose not to unit test the majority of code, hence there is definitely room for improvement here.

To productionize further in the future, I would include custom error messages and exceptions at both the script level and for my individual functions. For instance, if someone attempted to run `main.py` before they downloaded the data, I would include an error message instructing them to do so (or perhaps automatically check if data was downloaded, and if not, download data). Additionally, if someone downloaded the data already and tried to run `data_extraction.py` again, I would include a check confirming that they do indeed want to redownload.

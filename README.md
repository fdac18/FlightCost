# FlightCost
 Final project analyzing flight data from the Bureau of Transportation to compare average ticket costs across airports in TN.
## Proposal
[Overleaf](https://www.overleaf.com/19908399gnnxykdhzmbk)
## To-Do
- Determine *specific* goals for the project (i.e. what all do we want to present at the end of the semester? what kind of results will be most interesting to people?)

**Current thoughts:** 
 - User-Interface focus -> searchable, allows for user parameters
 - Current Location (City), Destination Location (City), # of passengers, willing to drive distance
 - Specify Dates
 - Return historical graph/representation for that ticket selection
 - Number of stops at that average price point
 - Average flight duration
 - Compare average ticket costs from 3 NEAREST airports to every major city in America.

## Data We Can Work With
- [This](https://www.transtats.bts.gov/databases.asp?pn=1&Mode_ID=1&Mode_Desc=Aviation&Subject_ID2=0) provides a list of all 26 databases that the Bureau of Transportation groups together under the umbrella of "Aviation"
- [This](https://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=125) is the "Airline Origin and Destination Survey" database description and [here](https://www.transtats.bts.gov/tables.asp?db_id=125&DB_Name=) are the tables of that database.

## Roles
### Beginning
- Getting the data, cleaning it, put it in CSVs originally -> Rojae, Andrey, Matt A.
- Data Analysis along with the responsibility of extracting the data -> Matt Kramer, Cai
- Visualizations -> Cai
- Platform Architect -> Everyone

### Later
- Move Data into DB
- UX
- Scraping LIVE data and storing it in our database

## Technology
- Python3
- IPython Notebooks
- Undecided SQL Database (Relational DB, mySQL?)
- Pandas, matplotlib, stats packages
- If we make it to scraping: Beautifulsoup, etc.
- If we make it to UX: Spyre

## Proposal Roles
- Objective and Motivation -> Cai
- Data -> Andrey
- Models and Algorithms -> Matt K., Rojae, Matt A.
- Time-line -> Everyone

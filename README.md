We all have heard about gerrymandering by now, but I've been dissatisfied with the current state of analysis of the fairness of Congressional districts. Specifically, proportionality is something that sounds fair in the abstract, but might result in suboptimal districts in a system where districts are drawn geographically (consider a state with a strong, uniform political lean; in this case, it would make sense for more districts to agree with that lean than the statewide proportional result).  

So, how many Congressional districts _should_ lean toward each party in any given state?  This is an attempt to answer that question by considering the partisanship of the nearest neighbors of each precinct.

This algorithm is as follows.  It draws the most compact possible Congressional district around each precinct in a state and calculates its two-party vote share.  It then declares that the number of Congressional districts that should lean toward each party should match the proportion of precincts whose most compact Congressional district leans toward that party.

To draw the most compact possible Congressional district around a precinct, the algorithm iteratively adds precincts to the Congressional district.  The starting point is the single precinct.  In each iteration, the geographic neighbors of the district are added to the district.  The iteration stops when the district contains at least as much population as the expected population of one Congressional district in the state. 

Currently, I've only run the algorithm on Massachusetts and Wisconsin (I haven't found a data set I like for a nation-wide analysis).  These states were chosen because they are both states where a proportional result might not be a fair result: Massachusetts is a state where the minority party has no compact Congressional district-size area of strength, meaning it's unrealistic to expect one third of Massachusetts Congressional districts to elect representatives from that party (and it might even be fair for no Congressional districts to lean toward the minority party); Wisconsin is a state split evenly but with extreme geographic polarization between its two large cities and its rural areas, forcing a choice between proportionality and not splitting the cities into multiple Congressional districts.

You should be able to just clone the repo and run `python3 massachusetts.py` or `python3 wisconsin.py` to see the results for yourself. 

They indicate that 99.1% of Massachusetts precincts would form the center of a Democratic-leaning congressional district.  Massachusetts has nine Congressional districts, so if this algorithm is a fair adjuticator of fairness, it's fair to expect that all of them would elect Democrats.  27.2% of Wisconsin precincts would form the center of a Democratic-leaning Congressional district, though, so by this algorithm one would expect only two (or maybe three) of Wisconsin's eight districts to elect Democrats.

Limitations of this analysis include:
- its results will be skewed when the population and geography of precincts correlate.  This is somewhat the case in Wisconsin.  As an extreme example, for a hypothetical state with 100 compact, adjacent rural precincts of 100 voters each and 1 urban precinct of 10000 voters.  Because there are more rural precincts, the algorithm would likely indicate that the statewide result should favor their preference.  

Data used for this analysis:
- Massachusetts:
  - Shapefile of precincts: [MassGIS](https://www.mass.gov/info-details/massgis-data-wards-and-precincts)
  - 2018 Senate election results by precinct: [MIT Election Data and Science Lab](https://github.com/MEDSL/2018-elections-official/blob/master/SENATE/SENATE_precinct_general.zip)
- Wisconsin:
  - Shapefile of precincts and election results: [Wisconsin state legislature](https://data-ltsb.opendata.arcgis.com/datasets/LTSB::2012-2020-election-data-with-2020-wards/explore?location=44.715441%2C-89.815220%2C8.00&showTable=true)

I used the 2018 Senate election for Massachusetts data because it is the post-2016 election that saw the weakest performance of any winning statewide candidate; I used 2020 presidential data for Wisconsin because the result was so close. 

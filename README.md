# Importing Trade Statistics Data from UN Comtrade Database
UN Comtrade is a rich database that holds trade statistics data on imports and exports of various goods from different countries.

Comtrade has an API that allows to easily download desired data in large quantities. Data can be pulled in csv or json formats. In cases when query results in an error, Comtrade also returns a descriptive error message (if downloading in json).

This sample code provides an example of a download routine with a log that keeps track of all successful downloads and all error messages.

Comtrade has bulk download options and premium access options, but this code follows the Public API such that it does not hit the API limits.

# Global Trade in Ice Cream
Ice cream is a good that is often produced and consumed locally. At the same time, it can be easily stored and transported. Let's find out which countries are the leading ice cream exporters and which countries are the main ice cream consumers.

Luckily, ice cream is indeed a good on which trade statistics is collected under the Harmonized System (HS) at the 6-digit level of aggregation (https://en.wikipedia.org/wiki/Harmonized_System).

    210500  Miscellaneous edible preparations // Ice cream and other edible ice, whether or not containing cocoa.

Let's use the following parameters for the API query:

    px=HS   // classification: Harmonized System
    cc=AG6  // aggregation: 6-digit
    r=...   // country code: will loop over them
    rg=...  // trade flow direction: will loop over 1 (imports) and 2 (exports)
    p=0     // partner country: 0 (world)
    freq=A  // frequency: annual
    ps=2015 // year: 2015
    fmt=json

Since it is not possible to pull data for individual products, let's download all data for a given country, year and trade direction, and then save individual files for imports and exports of product 210500 (ice cream).

## Ice Cream Trade Analysis
After firing up the code and waiting a while to download everything, let's explore the data.

The European countries seem to be at the lead in terms of both imports and exports of ice cream. The USA is also a big producer.

<img src="https://raw.githubusercontent.com/evpu/Comtrade-Download-Ice-Cream/master/ice_cream_bar.png" alt="Ice Cream: Top Importers and Exporters (Million $US)" width="600">

Most of the countries with large trade flows tend do export more ice cream than they import, with the exception of Spain and the United Kingdom.

<img src="https://raw.githubusercontent.com/evpu/Comtrade-Download-Ice-Cream/master/ice_cream_scatter.png" alt="Ice Cream: Scatterplot (Million $US)" width="500">

Notably, the distribution of prices per kilogram of ice cream is approximately the same for imports and exports.

<img src="https://raw.githubusercontent.com/evpu/Comtrade-Download-Ice-Cream/master/ice_cream_histogram.png" alt="Ice Cream: Price per Kilogram" width="600">

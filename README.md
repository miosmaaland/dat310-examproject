# dat310-examproject
Mio and Rich's exam project for Dat310


- Home
The home page has two functions. Function 1 is submitting movies. The user is allowed to write in any series they want, but have to choose between a set of options for the genres and platform and this will be submitted or added to the list of series. The other function is a search engine. The user can search for movie recommendations by choosing a genre and platform. They will then be sent to page results.html.

- Results 
This page displays the corresponding series to the earlier chosen genres and platforms. Here the user has the option to add a series to their own personal list by clicking on the "add to my list" button. This will send them to the "My List" page.

- My list
This page shows a list of all the series the user has added. Here the user has the option to delete series of their choosing from their own list.

- Trending
This page retrieves data from the tables searches and user_series2 in the database recommendations.db and uses it to set up 3 lists which display the most popular genres, platforms and series. It also shows how many times the genres and platforms have been searched and also how many times the series has been added to personal lists.

- Recommendations.db
    -user.series
    This table is used in 
# dat310-examproject
Mio and Rich's exam project for Dat310

- How to run the website?

To run the website you need to run the app.py and to access the website use the address given when running the code. You may also need to install "Flask" and "Werkzeug" using Pip before running the code.

- Instructions for testing
To test the website you can use the premade account. The username for the account is Mio and the password is Mio12345. You can also try the website without logging in, but you will not have some functions available like making personal lists. To nagivate around the page you can use the navbar on the top of the page. You can also register a new account and test how the trending and lists will change depending on what you do with different accounts. 

- functionality
    - Home
The home page is the main page and has two main functions. Function 1 is submitting movies. How this works is that there is a route in the app.py which takes the data the user gives about movies and inserts it into the table for series. The user is allowed to write in any series they want, but have to choose between a set of options for the genres and platform and this will be submitted or added to the list of series. The other function is a search engine. The user can search for movie recommendations by choosing a genre and platform. They will then be sent to the results page which will display a list of all the series which fit the criteria. 

    - Results 
This page displays the corresponding series to the earlier chosen genres and platforms. How this works is that the database has a table called series which split into three columns: name, genre and platform. When the user has picked a genre and platform the program will sort through the table for series and filter out the ones who do not contain the requiremnts. Here the user also has the option to add a series to their own personal list by clicking on the "add to my list" button. This will send them to the "My List" page with the added series.


- Register

If you have not registered already, you will have to register to be able to have a personal page. While having registered, you are logged in, which makes it able to save the searches you have done, the lists you have made with your personal favorites and also the profile image.
If trying to pick a username that is taken, you will get an error message regarding this. 
If trying to make a password that does not contain one big letter, one small letter, numbers and 8 characters, an error message will be received from this as well.


-Login
If you have a user that is registered, you are able to login to the account. Inside the app, while being logged in, you can do searches for different genres and platforms, in which you can add series to your list. Your lists will still be there if you log out and then log back in. You are also able to see your profile page, where your saved profile image will still be visible. 


    - My list
This page shows a list of all the series the user has added. The way this works is that when the user has chosen a series they want to add to their list and they click on the "add to my list" button. It sends that data into the tables calles user_series and user_series2. The user_series is used specifically in this page because there is a delete and update button. Here the user has the option to delete series or update the platform and genre of their series. When updated or deleted from this list it also deletes and updates the data from the user_series table.

    - Trending
This page retrieves data from the tables searches and user_series2 in the database recommendations.db and uses it to set up 3 lists which display the most popular genres, platforms and series bewteen all the users. It also shows how many times the genres and platforms have been searched and also how many times the series has been added to personal lists.

    - Profile 
    
    
 The profile page is made so that users are able to save their lists of tv series preferences. In this page the user will be able to upload a personal image, which will be linked to their user. In the personal page the Flask app are gathering the keys from the "user" table in the MySQL database, which connects the user to the profile image.



- Recommendations.db
In the setup_db.py we create 5 tables which are users, series, searches, user_series and user_series2. 
    - users
    This table is split into the three columns username, password and profile_image. This database is used when the user wants to register an new account. Then it inserts that data into the database. It is also used when a user logs in and checks if there is a corresponding account in the database. It is also used in the profile page then it inserts the uploaded picture to the table column.
    - series
    This table stores the information for series, platform and genres. It is used in the home page where you can submit series and it is also used in the result page where it displays all the data in the table.
    - searches
    This table is used to store all the search data the user gets when he searches for recommendations. It is also used in the trending page. In the trending it displays the data of the 5 most searched genres and platforms.
    - user_series2
    This table stores all the data the user gets when the user adds to their list in the series_list page. This is used in the trending page to display the 5 most added series to the users personal lists.
    - user_series
    This table stores all the data the user gets when the user adds to their list in the series_list page like in user_series2. The difference between user_series2 and user_series is that this table is specifically used for the series_list page and can be changed by deleting the added series on the page which will also delete the data in the table.


- Javascript
In the scripts.js, we are making sure that the app runs smoothly and dynamically. We have implemented Ajax requests, according to the principles of Rest API, on the front end by creating a "fetch" function that is gathering the genres and platforms while doing a search. The rest of the JavaScript is based on regular fluid implementations, as giving instructions on how to search for a series, by using both the genre and the platform e.g.

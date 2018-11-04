# Midterm - SI 364 F18

### Troy said it was alright to delete all classes, forms, routes and templates associated with 'Name'; therefore, you should not be looking for these in the application. 

## Instructions

This application uses the Ticketmaster Discovery API.

If you submit a city (Las Vegas, Chicago, Phoenix, Boston, etc.) you will find the top ten event results (or fewer, if there are less than ten associated results), each with respective:
	
	* `URL`
	* `Genre`
	* `Venue`

If you submit a keyword (Drake, Comedy, Basketball, Movie, Best, etc.) into the Keyword Entry fomm OR enter a keyword into the dynamic URL, you will find the top ten event results (or fewer, if there are less than ten associated results), each with respective:

	* `URL`
	* `Genre`
	* `Venue`

Finally, this application saves your results into two databases (events, venues).

The application should have the following routes, each rendering the template listed below:

* `http://localhost:5000/city_entry` -> `event_data.html`
* `http://localhost:5000/keyword_search` -> `keyword_entry.html`
* `http://localhost:5000/keyword_search/<keyword_entry>` -> `keyword_entry.html`
# Github Navigator
Github navigator is an application to search repository information on GitHub. The application uses GitHub developer API to search fetch repository information. API return top 5 repositories which are created recently based on the user search term. Application use python falcon framework on the backend for API call and angular js on the frontend for data representation.

Requirements
------------
* **Python**: 3.4+
* **falcon**: 2.0+
* **gunicorn**: 19.9.0+
* **requests**: 2.21.0
* **urllib3**: 1.24.3

Installation
------------
Create virtual environment to install dependancies

    python3 -m venv .env

Activate the environment

    source .env/bin/activate

Install dependencies

    pip install -r requirements.txt

Now everything is set up, enable web server on a specific port using gunicorn

    gunicorn application:api -b 0.0.0.0:8000

Open URL on a web browser.

Steps & Explanation
------------
index.html page contain javascript(angular js) and CSS(bootstrap) CDN link which provide single page application functionality.

1. Frontend page shows the input box where user can type the search keyword which check against repository name. Event trigger on pressing enter on the input box.

2. Frontend page makes a call to backend API('/api') using $http method on submit event with search term received from the input box.

3. Backend API('/api') received a call which search term. Search term then validated and encoded into a query_param format using urllib.

4. Encoded search param added into Github repository search URL and call it using python requests library. timeout setting use to close requests call after a particular threshold.

5. In response, we received the unsorted list of repository information. List of object sort using list sort and lambda function because created date which API received from GitHub is in string format. With the help of lambda function API sort list in descending order.

6. Top 5 result is returned to the frontend in response with last commit information. Last commit information not available in repository search API.

7. To fetch this information we use commit search API with limit 1 per page. In response, we will get last commit information which will be added in API response. Frontend received the response and based on response status fronted render data on the HTML page.

Why falcon?
Falcon is CPython based library which provides minimum dependencies to create REST API application. Falcon mainly used to create microservices.

Why angular js?
It's a single page web application which allows the user to render the page without reloading the complete page.


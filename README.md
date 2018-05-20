# Veturilo Statistics

Backend by [Wojtek Rymaszewski](https://github.com/wrymaszewski)

## Summary
Veturilo is a net of public bikes in Warsaw, Poland. However useful, sometimes it is difficult to predict the number of bikes and free stands at a given time and location. This Django app will perform cyclic scraping of the Veturilo website (https://www.veturilo.waw.pl/mapa-stacji/) to retrieve, and store the real-time data. Data can be then visualized using interactive plots and with the application of machine learning, predictions will be possible.

## Technologies/libraries
* Python
* Django
* Pandas
* BeautifulSoup
* Plotly
* ~~Celery~~
* HTML5
* CSS
* Javascript + JQuery

## To do
- [x] Web scraper
- [x] Interactive plots
- [x] Deployment
- [x] Frontend, RWD
- [x] REST API
- [ ] Machine learning module

## CLI commands
This app has been deployed to Python Anywhere: [Veturilo Stats](http://wrymaszewski.pythonanywhere.com).
I has begun collecting data.
The app can be also previewed on a local machine. Steps required are listed below:

1. Download and install Python [Anaconda] distribution (https://www.anaconda.com/download/#linux)
2. Create a virual environent in your terminal:
    ```bash
    conda create --name <environment_name>
    ```
    <!-- do not delete that slash below! -->
3. Activate the environment:\
    (Windows)
    ```bash
    activate <environment_name>
    ```
    (MacOS, Linux)
    ```bash
    source activate <environment_name>
    ```
4. Clone the repo:
    ```bash
    git clone <https://github.com/wrymaszewski/veturilo.git>
    ```
5. Go to the main folder

6. Install PIP and dependencies:
    ```bash
    conda install -c anaconda pip
    pip install -r requirements.txt
    ```
7. Start the server:
    ```bash
    python manage.py runserver
    ```
    local server setup default address is <http://127.0.0.1:8000/>.
    
## API documentation
You can retrieve the collected data using the Django REST Framework functionalities.

#### Collection of all locations
<http://wrymaszewski.pythonanywhere.com/scraper/api/locations> human-readible form
<http://wrymaszewski.pythonanywhere.com/scraper/api/locations/?format=json> JSON

#### Collection of a particular location - you need to use a primary key from the database (pk)
<http://wrymaszewski.pythonanywhere.com/scraper/api/location/(pk)> human-readible form
<http://wrymaszewski.pythonanywhere.com/scraper/api/location/(pk)/?format=json> JSON

#### Collection of all snapshots (it will take a lot of time!)
<http://wrymaszewski.pythonanywhere.com/scraper/api/snapshots> human-readible form
<http://wrymaszewski.pythonanywhere.com/scraper/api/snapshots/?format=json> JSON

#### Collection of a particular snapshot - you need to use a primary key from the database (pk)
<http://wrymaszewski.pythonanywhere.com/scraper/api/snapshot/(pk)> human-readible form
<http://wrymaszewski.pythonanywhere.com/scraper/api/snapshot/(pk)/?format=json> JSON
    
#### Collection of all monthly statistics (If there are any available)
<http://wrymaszewski.pythonanywhere.com/scraper/api/stats> human-readible form
<http://wrymaszewski.pythonanywhere.com/scraper/api/stats/?format=json> JSON

#### Collection of a particular monthly statistic - you need to use a primary key from the database (pk)
<http://wrymaszewski.pythonanywhere.com/scraper/api/stat/(pk)> human-readible form
<http://wrymaszewski.pythonanywhere.com/scraper/api/stat/(pk)/?format=json> JSON    



# mid project bdmlpt1021
## COVID-19

### **Task list**

- [x] L1: Crear api en fastapi
- [x] L1: Crear dashboard en streamlit
- [x] L1: Base de datos en MongoDB o PostgreSQL
- [x] L2: Utilizar de datos geoespaciales y geoqueries en MongoDB o Postgres (Usando PostGIS)*
- [x] L2: Tener la base de datos en el Cloud (Hay servicios gratis en MongoDB Atlas, Heroku Postgres, dentre otros)
- [x] L2: Generar reporte pdf de los datos visibles en Streamlit, descargable mediante boton.
- [x] L2: Un dashboard de multiples páginas en Streamlit
- [x] L3: Que el dashboard te envie el reporte pdf por e-mail
- [x] L3: Poder subir nuevos datos a la bbdd via la API (usuario y contraseña como headers del request)
- [x] L4: Poder actualizar la base de datos via Streamlit (con usuario y contraseña, en una página a parte. El dashboard  debe hacer la petición anterior que añade datos via API)
- [x] L4: Crear contenedor Docker y hacer deploy de los servicios en el cloud (Heroku. Los dos servicios deben subirse separadamente)
- [ ] L5: Controlar el pipeline con Apache Airflow

*This data is impossible to get geoqueries, because the different coordinate points are too far.
### **INDEX**
1. [API](#api)
    1. [API Structured](#api-structured)
1. [MONGO](#mongo)
1. [DASHBOARD](#dashboard)
    1. [DASHBOARD Structured](#dashboard-structured)
1. [PRE-COMMIT](#pre-commit)
1. [REFERENCES](#references)


### **API**
The API has different endpoints: You can have the documentation of the api [here](https://mid-api-covid.herokuapp.com/docs#/).
The API is divided by cases, deaths and recoveries. It has other endpoints that are common for example the internals endpoint can use to CRUD requests.

To run the api in your local machine you need a conda virtual environment (best option), install the requirements with pip:
```bash
$ pip install -r requirements.txt
```
When the last command finished you only need to run the following command inside the `api/src` directory:
```bash
uvicorn main:app --reload
```
And you can go to [http://localhost:8000/docs](http://localhost:8000/docs) to get the api correctly running.

You need the following environment variables or put a `.env` file in the `api/src` directory:
- MONGO_URI -> The mongo url with the user and pass to get the information.
- MONGO_DB -> The database where thhe information is stored.
- MONGO_COL -> The collection of the database.
- API_KEY -> Api key used to access to the internals uris.

#### **API Structured**
```
.
├── Dockerfile
├── requirements.txt -> Dependencies
└── src -> The directory with all the code.
    ├── config.py -> Configure the variables (".env" or with "os.getenv").
    ├── db -> All the scripts to connect with mongodb
    │   ├── db.py
    │   └── __init__.py
    ├── __init__.py
    ├── internals
    │   └── internal_operations.py -> Internal endpoints with authentication
    ├── main.py -> Principal app to run Fastapi
    ├── models -> The different models uses to validate the schema response for each endpoint.
    │   ├── confirmed_model.py
    │   ├── deaths_model.py
    │   ├── __init__.py
    │   ├── internals_model.py
    │   └── recoveries_model.py
    ├── routers -> The different FastApi routers with its respective endpoints.
    │   ├── common.py
    │   ├── confirmed_cases.py
    │   ├── deaths.py
    │   ├── __init__.py
    │   └── recoveries.py
    └── utils -> Utilities to use (time_response.py can get the response time on a header)
        ├── functutils.py
        ├── __init__.py
        └── time_response.py
```

### **MONGO**
It's deployed using mongo atlas in a shared cluster.

Each mongo document has the following structured:
```json
{
    "country": "country",
    "date": "date",
    "cases": "cases_per_day",
    "cases_accumulated": "total_cases",
    "deaths": "deaths_per_day",
    "deaths_accumulated": "total_deaths",
    "recoveries": "recoveries_per_day",
    "recoveries_accumulated": "total_recoveries",
    "latitude": "lat",
    "longitude": "long",
    "location":
        {
            "type": "Point",
            "coordinates": ["long", "lat"]
        }
}
```

It has a GEOSPHERE index to make the possibility to geoqueries. Also, the mongo has two more index:
- Index in the date field.
- Index compound by country and date fields.

### **DASHBOARD**
The dashboard has made with streamlit and it's divided in multipages:
- Home -> Home page (Nothing more to explain here).
- Cases -> Cases page. Here you can navigate and select the countries with a date range, you can see the different options in the sidebar to get different results. The results were the cases per each country.
- Deaths -> Deaths page. Here you can navigate and select the countries with a date range, you can see the different options in the sidebar to get different results. The results were the deaths per each country.
- Recoveries -> Recoveries page. Here you can navigate and select the countries with a date range, you can see the different options in the sidebar to get different results. The results were the recoveries per each country.
- Report -> Here you can select a date range and a some countries, you can download the pdf or with a password you can send it by email.
- Maps -> Here you can select between cases, deaths and recoveries and a date and show a map with heatmap with the cases, deaths or recoveries for the date selected.
- Internals -> Here you can update, create and delete a row. Providing a password.

To run the dashboard in your local machine you need a conda virtual environment and install the packages provided in the `dashboard/requirements.txt` file.
```bash
$ pip install -r requirements.txt
```
When you install all the required packages you can get the dashboard up and running executing the following command inside the directory `dashboard/src/`:
```bash
$ streamlit run main.py
```
You need the following environment variables:
- MJ_APIKEY_PUBLIC -> The public api key to configure mailjet.
- MJ_APIKEY_PRIVATE -> The secret api key to auth with mailjet.
- USER_PASS -> The password used to get into the internals page.
- API_KEY -> Api key used to connect with the authentication endpoints.
- API_URL -> Api URL used by streamlit to get the information
- MAIL -> From mail used from mailjet to send emails.

#### **Dashboard Structured**
```
├── Dockerfile
├── requirements.txt -> Dependencies
├── src -> Dashboard source code
│   ├── config.py -> Configure some environment variables
│   ├── data -> Uses to request to the different api endpoints.
│   │   └── funcdata.py
│   ├── main.py -> Principal app.
│   ├── multiapp.py -> Multipage class
│   ├── pages -> The different pages.
│   │   ├── cases.py
│   │   ├── deaths.py
│   │   ├── home.py
│   │   ├── internals.py
│   │   ├── maps.py
│   │   ├── pdf_report.html -> This html is here to generate the pdf report with Jinja2.
│   │   ├── recoveries.py
│   │   └── report.py
│   └── utils -> Utilies to use.
│       ├── funcutils.py
│       └── streamlit_utils.py -> Some functions to avoid repetition on some pages.
└── start.sh -> Script used to deploy in heroku. (The $PORT is needed).
```

### **Pre-commit**
This pre-commit is used to get good practices on python coding. It uses the following modules:
- https://github.com/psf/black -> Code formatted.
- https://flake8.pycqa.org/en/latest/ -> Code style guide.
- https://github.com/PyCQA/isort -> Sort import alphabetically.
- The `setup.cfg` has the configuration for flake8 and isort.

### REFERENCES
- https://docs.streamlit.io/library/get-started
- https://plotly.com/python/
- https://pydeck.gl/gallery/heatmap_layer.html
- https://towardsdatascience.com/deploying-a-basic-streamlit-app-to-heroku-be25a527fcb3
- https://github.com/marketplace/actions/deploy-to-heroku
- https://seaborn.pydata.org/generated/seaborn.heatmap.html
- https://fastapi.tiangolo.com/
- https://altair-viz.github.io/getting_started/overview.html
- https://pydantic-docs.helpmanual.io/
- https://fastapi.tiangolo.com/advanced/custom-request-and-route/?h=time#custom-apiroute-class-in-a-router
- https://towardsdatascience.com/4-pre-commit-plugins-to-automate-code-reviewing-and-formatting-in-python-c80c6d2e9f5
- https://pycqa.github.io/isort/docs/configuration/pre-commit.html
- https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/

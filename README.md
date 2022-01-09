# mid project bdmlpt1021
## COVID-19

### Task list

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
- [] L5: Controlar el pipeline con Apache Airflow

*This data is impossible to get geoqueries, because the different coordinate points are too far.

### API
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

### MONGO
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
            'type': 'Point',
            'coordinates': ["long", "lat"]
        }
}
```

It has a GEOSPHERE index to make the possibility to geoqueries. Also, the mongo has two more index:
- Index in the date field.
- Index compound by country and date fields.

### DASHBOARD
Explain dashboard

### REFERENCES
- https://docs.streamlit.io/library/get-started
- https://plotly.com/python/
- https://pydeck.gl/gallery/heatmap_layer.html
- https://towardsdatascience.com/deploying-a-basic-streamlit-app-to-heroku-be25a527fcb3
- https://github.com/marketplace/actions/deploy-to-heroku
- https://seaborn.pydata.org/generated/seaborn.heatmap.html

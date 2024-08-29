![INTERFACE](https://github.com/dragonlee97/citibike_api/blob/main/interface.png?raw=true)
FastAPI application designed to query aggregated data from the BigQuery Citibike dataset

<be>

# Prerequisites & Set up
- You should have a gcp account
- Create a personal project, and a dataset dedicated for this API
- Copy the public dataset tables `bigquery-public-data.new_york_citibike.trips` into the above dataset and still name it trips
- Create a users table under the same personal dataset with the following schema
  
| FieldName | Type       |
|-----------|------------|
| username  | STRING     |
| password  | STRING     |
| created_at| TIMESTAMP  |

- Create a .env file and add two variables: `PROJECT` and `DATASET` of where your tables locate
- Launch the API by the command `docker compose up` and go the port `localhost:8000/docs` on your browser
- If it is your first login. Go to the `Users` route and use the `try it out` feature to create your username and password
- Click on Authorize on the top right corner of the page and login with the credentials you just created
  
# API route specifications
## Insight
### user_demographics
This is a get API request without parameters, which returns the number of users for 6 demographic categories respectively.

### station_traffic
This is a post API request which takes four parameters: `request_id`, `station`, `start_date` and `end_date`. The first two are required and the last two are optional. Please find the example request when you unfold the section.

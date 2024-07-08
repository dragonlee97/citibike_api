SELECT
    SUM(CASE WHEN start_station_name = '{{ station_request.station }}' THEN 1 ELSE 0 END) AS departures,
    SUM(CASE WHEN end_station_name = '{{ station_request.station }}' THEN 1 ELSE 0 END) AS arrivals
FROM `{{ project }}.{{ dataset }}.trips` t
{% if station_request.start_date and station_request.end_date %}
WHERE DATE(starttime) BETWEEN '{{ station_request.start_date }}' AND '{{ station_request.end_date }}'
{% elif station_request.start_date %}
WHERE DATE(starttime)>='{{ station_request.start_date }}'
{% elif station_request.end_date %}
WHERE DATE(starttime)<='{{ station_request.end_date }}'
{% else %}
{% endif %}


import responses

from aqi_producer import (
    fetch_aqi_data
)

@responses.activate
def test_fetch_aqi_data():

    responses.add(

        responses.GET,

        "http://api.openweathermap.org/data/2.5/air_pollution",

        json={
            "list": [
                {
                    "main": {
                        "aqi": 2
                    },

                    "components": {
                        "pm2_5": 15.0,
                        "pm10": 20.0
                    }
                }
            ]
        },

        status=200
    )

    data = fetch_aqi_data()

    assert data["aqi"] == 2

    assert data["pm25"] == 15.0

    assert data["pm10"] == 20.0
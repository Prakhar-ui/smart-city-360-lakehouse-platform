import responses

from weather_producer import (
    fetch_weather_data
)

@responses.activate
def test_fetch_weather_data():

    responses.add(

        responses.GET,

        "https://api.openweathermap.org/data/2.5/weather",

        json={
            "main": {
                "temp": 28,
                "humidity": 70,
                "pressure": 1000
            },

            "weather": [
                {"main": "Clouds"}
            ],

            "wind": {
                "speed": 5
            }
        },

        status=200
    )

    data = fetch_weather_data()

    assert data["temperature"] == 28

    assert data["humidity"] == 70

    assert data["weather_condition"] == "Clouds"
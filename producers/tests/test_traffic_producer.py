import responses

from traffic_producer import (
    fetch_traffic_data
)

@responses.activate
def test_fetch_traffic_data():

    responses.add(

        responses.GET,

        "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json",

        json={
            "flowSegmentData": {
                "currentSpeed": 30,
                "freeFlowSpeed": 60
            }
        },

        status=200
    )

    data = fetch_traffic_data()

    assert data["current_speed"] == 30

    assert data["free_flow_speed"] == 60

    assert (
        data["congestion_percentage"]
        == 50.0
    )
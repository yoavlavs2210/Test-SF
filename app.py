from flask import Flask, request
import requests

def get_weather():
    API_KEY = "682f2eff065b4210a7d72530241605"
    # The city you want to get weather for
    CITY = "Tel Aviv"

    # The base URL for the WeatherAPI.com API
    base_url = "http://api.weatherapi.com/v1/current.json"

    # Parameters for the API request: API key and city name
    params = {
        "key": API_KEY,
        "q": CITY
    }

    temp_c = ""
    try:
        # Make the GET request to the API
        response = requests.get(base_url, params=params, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            weather_data = response.json()

            # Extract relevant information
            temp_c = weather_data['current']['temp_c']
        else:
            print(f"Error fetching weather data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            temp_c = f"Response: {response.text}"

    except requests.exceptions.RequestException as e:
        # Handle network or other request-related errors
        print(f"An error occurred: {e}")
    return temp_c




# Create a Flask application instance
app = Flask(__name__)

# Define a route for the homepage
@app.route("/")
def print_message():
    client_ip = ""
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        # Direct request without proxy
        client_ip = request.remote_addr
    #client_ip = request.headers.getlist("X-Forwarded-For")[0]
    weather = get_weather()
    return f"Hello {client_ip} and welcome to silver. The weather today in TLV is {weather} C"

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


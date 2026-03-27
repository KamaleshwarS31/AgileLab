# Weather API Test Suite

This directory contains an automated testing suite for the Weather Application Backend using **Maven**, **JUnit 5**, and **REST Assured**.

## Prerequisites

Before running the tests, ensure that the backend server is running. It must be accessible at `http://localhost:8000`.

To start the backend, you can use your startup script from the project root:
```powershell
.\start.ps1
```

## Running the Tests

To run the automated test suite, execute the following command in this directory (`maven-app`):

```powershell
mvn clean test
```

## Test Definitions

The tests are defined in `src/test/java/com/weatherapp/WeatherApiTest.java`. Currently, they validate the following core API endpoints:

1. **Get Current Weather**: Tests the `/api/weather/current` endpoint with coordinates to ensure a 200 OK status and correct response schema.
2. **Get Forecast**: Tests the `/api/weather/forecast` endpoint with coordinates for the 7-day forecast format.
3. **Search Locations**: Tests the `/api/locations/search` endpoint by querying a city name and validating the result matches the query.

## Adding New Tests

You can add more API endpoint tests (like Favories interaction) in the `WeatherApiTest.java` class using the standard `given/when/then` syntax provided by REST Assured.

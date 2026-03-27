package com.weatherapp;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class WeatherApiTest {

    @BeforeAll
    public static void setup() {
        // Set the base URI to the FastAPI backend running locally
        RestAssured.baseURI = "http://localhost:8000";
    }

    @Test
    @DisplayName("Test getting current weather for a valid location")
    public void testGetCurrentWeather() {
        // We will test using coordinates for London (lat=51.5072, lon=-0.1276)
        given()
            .queryParam("lat", 51.5072)
            .queryParam("lon", -0.1276)
        .when()
            .get("/api/weather/current")
        .then()
            .statusCode(200)
            .body("location", notNullValue())
            .body("temperature", notNullValue())
            .body("weather.main", notNullValue());
    }

    @Test
    @DisplayName("Test getting forecast for a valid location")
    public void testGetForecast() {
        // Test forecast for London
        given()
            .queryParam("lat", 51.5072)
            .queryParam("lon", -0.1276)
        .when()
            .get("/api/weather/forecast")
        .then()
            .statusCode(200)
            .body("hourly", notNullValue())
            .body("daily", notNullValue())
            .body("timezone", notNullValue());
    }

    @Test
    @DisplayName("Test search locations endpoint")
    public void testSearchLocations() {
        // Test searching for 'London'
        given()
            .queryParam("q", "London")
        .when()
            .get("/api/locations/search")
        .then()
            .statusCode(200)
            // It should return an array of locations
            .body("size()", greaterThan(0))
            .body("[0].name", containsString("London"));
    }
}

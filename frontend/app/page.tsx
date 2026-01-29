'use client';

import { useState, useEffect } from 'react';
import { CurrentWeather, Forecast, Location, FavoriteLocation } from '@/types/weather';
import { weatherAPI } from '@/lib/api';
import { getUserId } from '@/lib/utils';
import WeatherCard from '@/components/WeatherCard';
import DailyForecast from '@/components/DailyForecast';
import LocationSearch from '@/components/LocationSearch';
import styles from './page.module.css';

export default function Home() {
  const [currentWeather, setCurrentWeather] = useState<CurrentWeather | null>(null);
  const [forecast, setForecast] = useState<Forecast | null>(null);
  const [favorites, setFavorites] = useState<FavoriteLocation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [currentLocation, setCurrentLocation] = useState<{ lat: number; lon: number } | null>(null);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);

    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme') as 'dark' | 'light' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute('data-theme', savedTheme);
    }

    // Get user's current location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const coords = {
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          };
          setCurrentLocation(coords);
          loadWeatherData(coords.lat, coords.lon);
        },
        (error) => {
          console.error('Error getting location:', error);
          // Default to New York if geolocation fails
          loadWeatherData(40.7128, -74.0060);
        }
      );
    } else {
      // Default to New York if geolocation not supported
      loadWeatherData(40.7128, -74.0060);
    }

    // Load favorites
    loadFavorites();
  }, []);

  const loadWeatherData = async (lat: number, lon: number) => {
    setIsLoading(true);
    setError(null);

    try {
      const [weatherData, forecastData] = await Promise.all([
        weatherAPI.getCurrentWeather(lat, lon),
        weatherAPI.getForecast(lat, lon),
      ]);

      setCurrentWeather(weatherData);
      setForecast(forecastData);
    } catch (err) {
      console.error('Error loading weather data:', err);
      setError('Failed to load weather data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const loadFavorites = async () => {
    try {
      const userId = getUserId();
      const favs = await weatherAPI.getFavorites(userId);
      setFavorites(favs);
    } catch (err) {
      console.error('Error loading favorites:', err);
    }
  };

  const handleLocationSelect = (location: Location) => {
    loadWeatherData(location.latitude, location.longitude);
    setCurrentLocation({ lat: location.latitude, lon: location.longitude });
  };

  const handleUseCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const coords = {
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          };
          setCurrentLocation(coords);
          loadWeatherData(coords.lat, coords.lon);
        },
        (error) => {
          console.error('Error getting location:', error);
          alert('Unable to get your location. Please enable location services.');
        }
      );
    }
  };

  const handleToggleFavorite = async () => {
    if (!currentWeather) return;

    const userId = getUserId();
    const isFavorite = favorites.some(
      (fav) =>
        fav.latitude === currentWeather.latitude &&
        fav.longitude === currentWeather.longitude
    );

    try {
      if (isFavorite) {
        const favorite = favorites.find(
          (fav) =>
            fav.latitude === currentWeather.latitude &&
            fav.longitude === currentWeather.longitude
        );
        if (favorite) {
          await weatherAPI.deleteFavorite(favorite.id, userId);
        }
      } else {
        await weatherAPI.addFavorite(userId, {
          name: currentWeather.location,
          country: currentWeather.country,
          latitude: currentWeather.latitude,
          longitude: currentWeather.longitude,
        });
      }
      loadFavorites();
    } catch (err) {
      console.error('Error toggling favorite:', err);
    }
  };

  const handleFavoriteClick = (favorite: FavoriteLocation) => {
    loadWeatherData(favorite.latitude, favorite.longitude);
    setCurrentLocation({ lat: favorite.latitude, lon: favorite.longitude });
  };

  const handleRemoveFavorite = async (favoriteId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const userId = getUserId();
      await weatherAPI.deleteFavorite(favoriteId, userId);
      loadFavorites();
    } catch (err) {
      console.error('Error removing favorite:', err);
    }
  };

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  };

  const isFavorite = currentWeather
    ? favorites.some(
      (fav) =>
        fav.latitude === currentWeather.latitude &&
        fav.longitude === currentWeather.longitude
    )
    : false;

  return (
    <main className={styles.main}>
      <div className={styles.backgroundGradient}></div>

      <div className={styles.container}>
        <header className={styles.header}>
          <h1 className={styles.title}>🌤️ Weather Forecast</h1>
          <p className={styles.subtitle}>
            Get accurate weather forecasts with beautiful visualizations and detailed insights
          </p>
        </header>

        <div className={styles.searchSection}>
          <LocationSearch
            onLocationSelect={handleLocationSelect}
            onUseCurrentLocation={handleUseCurrentLocation}
          />
        </div>

        {isLoading ? (
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            <p className={styles.loadingText}>Loading weather data...</p>
          </div>
        ) : error ? (
          <div className={styles.error}>
            <h3 className={styles.errorTitle}>⚠️ Error</h3>
            <p className={styles.errorMessage}>{error}</p>
            <button
              className={styles.retryBtn}
              onClick={() => currentLocation && loadWeatherData(currentLocation.lat, currentLocation.lon)}
            >
              Retry
            </button>
          </div>
        ) : (
          <div className={styles.content}>
            {currentWeather && (
              <div className={styles.weatherSection}>
                <WeatherCard
                  weather={currentWeather}
                  onToggleFavorite={handleToggleFavorite}
                  isFavorite={isFavorite}
                />
              </div>
            )}

            {forecast && forecast.daily.length > 0 && (
              <div className={styles.forecastSection}>
                <DailyForecast forecast={forecast.daily} />
              </div>
            )}

            {favorites.length > 0 && (
              <div className={styles.favoritesSection}>
                <h3 className={styles.favoritesTitle}>⭐ Favorite Locations</h3>
                <div className={styles.favoritesGrid}>
                  {favorites.map((favorite) => (
                    <div
                      key={favorite.id}
                      className={styles.favoriteItem}
                      onClick={() => handleFavoriteClick(favorite)}
                    >
                      <div className={styles.favoriteInfo}>
                        <div className={styles.favoriteName}>
                          📍 {favorite.location_name}
                        </div>
                        <div className={styles.favoriteCountry}>
                          {favorite.country}
                        </div>
                      </div>
                      <button
                        className={styles.removeBtn}
                        onClick={(e) => handleRemoveFavorite(favorite.id, e)}
                        title="Remove from favorites"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <button className={styles.themeToggle} onClick={toggleTheme} title="Toggle theme">
        {theme === 'dark' ? '☀️' : '🌙'}
      </button>
    </main>
  );
}

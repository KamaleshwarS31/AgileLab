'use client';

import { CurrentWeather } from '@/types/weather';
import { formatTemperature, formatTime, getWeatherIcon, getWindDirection } from '@/lib/utils';
import styles from './WeatherCard.module.css';
import { useState } from 'react';

interface WeatherCardProps {
    weather: CurrentWeather;
    onToggleFavorite?: () => void;
    isFavorite?: boolean;
}

export default function WeatherCard({ weather, onToggleFavorite, isFavorite = false }: WeatherCardProps) {
    const [isHovered, setIsHovered] = useState(false);

    return (
        <div
            className={styles.weatherCard}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <div className={styles.content}>
                <div className={styles.header}>
                    <div className={styles.location}>
                        <h2 className={styles.locationName}>
                            📍 {weather.location}
                        </h2>
                        <p className={styles.country}>{weather.country}</p>
                    </div>
                    {onToggleFavorite && (
                        <button
                            className={`${styles.favoriteBtn} ${isFavorite ? styles.active : ''}`}
                            onClick={onToggleFavorite}
                            aria-label={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                        >
                            {isFavorite ? '⭐' : '☆'}
                        </button>
                    )}
                </div>

                <div className={styles.mainWeather}>
                    <div className={styles.temperature}>
                        <div className={styles.tempValue}>
                            {formatTemperature(weather.temperature)}
                        </div>
                        <div className={styles.feelsLike}>
                            Feels like {formatTemperature(weather.feels_like)}
                        </div>
                    </div>

                    <div className={styles.weatherIcon}>
                        <img
                            src={getWeatherIcon(weather.weather.icon)}
                            alt={weather.weather.description}
                            className={styles.iconImage}
                        />
                        <p className={styles.description}>{weather.weather.description}</p>
                    </div>
                </div>

                <div className={styles.details}>
                    <div className={styles.detailItem}>
                        <span className={styles.detailLabel}>High / Low</span>
                        <span className={styles.detailValue}>
                            {formatTemperature(weather.temp_max)} / {formatTemperature(weather.temp_min)}
                        </span>
                    </div>

                    <div className={styles.detailItem}>
                        <span className={styles.detailLabel}>Humidity</span>
                        <span className={styles.detailValue}>
                            💧 {weather.humidity}%
                        </span>
                    </div>

                    <div className={styles.detailItem}>
                        <span className={styles.detailLabel}>Wind</span>
                        <span className={styles.detailValue}>
                            🌬️ {weather.wind_speed} m/s {getWindDirection(weather.wind_deg)}
                        </span>
                    </div>

                    <div className={styles.detailItem}>
                        <span className={styles.detailLabel}>Pressure</span>
                        <span className={styles.detailValue}>
                            🌡️ {weather.pressure} hPa
                        </span>
                    </div>

                    <div className={styles.detailItem}>
                        <span className={styles.detailLabel}>Clouds</span>
                        <span className={styles.detailValue}>
                            ☁️ {weather.clouds}%
                        </span>
                    </div>

                    {weather.visibility && (
                        <div className={styles.detailItem}>
                            <span className={styles.detailLabel}>Visibility</span>
                            <span className={styles.detailValue}>
                                👁️ {(weather.visibility / 1000).toFixed(1)} km
                            </span>
                        </div>
                    )}
                </div>

                <div className={styles.sunTimes}>
                    <div className={styles.sunTime}>
                        <div className={styles.sunIcon}>🌅</div>
                        <div className={styles.sunInfo}>
                            <span className={styles.sunLabel}>Sunrise</span>
                            <span className={styles.sunValue}>{formatTime(weather.sunrise)}</span>
                        </div>
                    </div>

                    <div className={styles.sunTime}>
                        <div className={styles.sunIcon}>🌇</div>
                        <div className={styles.sunInfo}>
                            <span className={styles.sunLabel}>Sunset</span>
                            <span className={styles.sunValue}>{formatTime(weather.sunset)}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

'use client';

import { DailyForecast as DailyForecastType } from '@/types/weather';
import { formatDate, formatTemperature, getWeatherIcon } from '@/lib/utils';
import styles from './DailyForecast.module.css';

interface DailyForecastProps {
    forecast: DailyForecastType[];
}

export default function DailyForecast({ forecast }: DailyForecastProps) {
    return (
        <div className={styles.forecastContainer}>
            <div className={styles.header}>
                <h3 className={styles.title}>📅 7-Day Forecast</h3>
            </div>

            <div className={styles.forecastGrid}>
                {forecast.map((day, index) => (
                    <div key={day.dt} className={styles.forecastItem}>
                        <div className={styles.day}>
                            {index === 0 ? 'Today' : formatDate(day.dt)}
                        </div>

                        <img
                            src={getWeatherIcon(day.weather.icon)}
                            alt={day.weather.description}
                            className={styles.icon}
                        />

                        <div className={styles.temps}>
                            <span className={styles.tempHigh}>
                                {formatTemperature(day.temp_max)}
                            </span>
                            <span className={styles.tempLow}>
                                {formatTemperature(day.temp_min)}
                            </span>
                        </div>

                        <p className={styles.description}>{day.weather.description}</p>

                        {day.pop > 0 && (
                            <div className={styles.precipitation}>
                                <span>💧</span>
                                <span>{Math.round(day.pop * 100)}%</span>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

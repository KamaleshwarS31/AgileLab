export interface WeatherCondition {
  id: number;
  main: string;
  description: string;
  icon: string;
}

export interface CurrentWeather {
  location: string;
  country: string;
  latitude: number;
  longitude: number;
  temperature: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  pressure: number;
  humidity: number;
  wind_speed: number;
  wind_deg: number;
  clouds: number;
  visibility?: number;
  weather: WeatherCondition;
  sunrise: number;
  sunset: number;
  timezone: number;
  dt: number;
}

export interface HourlyForecast {
  dt: number;
  temperature: number;
  feels_like: number;
  pressure: number;
  humidity: number;
  clouds: number;
  wind_speed: number;
  wind_deg: number;
  weather: WeatherCondition;
  pop: number;
  rain?: number;
  snow?: number;
}

export interface DailyForecast {
  dt: number;
  sunrise: number;
  sunset: number;
  temp_day: number;
  temp_min: number;
  temp_max: number;
  temp_night: number;
  temp_eve: number;
  temp_morn: number;
  feels_like_day: number;
  feels_like_night: number;
  feels_like_eve: number;
  feels_like_morn: number;
  pressure: number;
  humidity: number;
  wind_speed: number;
  wind_deg: number;
  clouds: number;
  pop: number;
  rain?: number;
  snow?: number;
  weather: WeatherCondition;
  uvi?: number;
}

export interface Forecast {
  latitude: number;
  longitude: number;
  timezone: string;
  hourly: HourlyForecast[];
  daily: DailyForecast[];
}

export interface Location {
  name: string;
  country: string;
  state?: string;
  latitude: number;
  longitude: number;
}

export interface FavoriteLocation {
  id: number;
  location_id: number;
  location_name: string;
  country: string;
  latitude: number;
  longitude: number;
  created_at: string;
}

export interface HistoricalWeather {
  timestamp: string;
  temperature: number;
  feels_like: number;
  pressure: number;
  humidity: number;
  wind_speed: number;
  weather_main: string;
  weather_description: string;
}

export interface Coordinates {
  latitude: number;
  longitude: number;
}

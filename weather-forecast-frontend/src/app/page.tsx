"use client";

import { useEffect, useState } from "react";
// import SearchBar from "@/components/SearchBar";
// import WeatherCard from "@/components/WeatherCard";

export default function Home() {
  const [mounted, setMounted] = useState(false);
  const [city, setCity] = useState("");

  // ✅ ensures client-only rendering
  useEffect(() => {
    setMounted(true);
  }, []);

  // ⛔ prevent server/client mismatch
  if (!mounted) return null;

  return (
    <main className="min-h-screen flex flex-col items-center p-6">
      <h1 className="text-4xl font-bold mb-6">🌦 Weather Forecast</h1>

      {/* <SearchBar onSearch={setCity} />

      {city && <WeatherCard city={city} />} */}
    </main>
  );
}

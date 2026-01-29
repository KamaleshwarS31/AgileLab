'use client';

import { useState, useEffect, useRef } from 'react';
import { Location } from '@/types/weather';
import { weatherAPI } from '@/lib/api';
import styles from './LocationSearch.module.css';

interface LocationSearchProps {
    onLocationSelect: (location: Location) => void;
    onUseCurrentLocation?: () => void;
}

export default function LocationSearch({ onLocationSelect, onUseCurrentLocation }: LocationSearchProps) {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Location[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [showResults, setShowResults] = useState(false);
    const searchRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
                setShowResults(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    useEffect(() => {
        const searchLocations = async () => {
            if (query.length < 2) {
                setResults([]);
                setShowResults(false);
                return;
            }

            setIsLoading(true);
            try {
                const locations = await weatherAPI.searchLocations(query);
                setResults(locations);
                setShowResults(true);
            } catch (error) {
                console.error('Error searching locations:', error);
                setResults([]);
            } finally {
                setIsLoading(false);
            }
        };

        const debounce = setTimeout(searchLocations, 300);
        return () => clearTimeout(debounce);
    }, [query]);

    const handleSelectLocation = (location: Location) => {
        onLocationSelect(location);
        setQuery('');
        setShowResults(false);
    };

    return (
        <div className={styles.searchContainer} ref={searchRef}>
            <div className={styles.searchWrapper}>
                <span className={styles.searchIcon}>🔍</span>
                <input
                    type="text"
                    className={styles.searchInput}
                    placeholder="Search for a city..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onFocus={() => results.length > 0 && setShowResults(true)}
                />
                {onUseCurrentLocation && (
                    <button
                        className={styles.locationBtn}
                        onClick={onUseCurrentLocation}
                        title="Use current location"
                    >
                        📍
                    </button>
                )}
            </div>

            {showResults && (
                <div className={styles.resultsDropdown}>
                    {isLoading ? (
                        <div className={styles.loading}>
                            <div className={styles.spinner}></div>
                            <span>Searching...</span>
                        </div>
                    ) : results.length > 0 ? (
                        results.map((location, index) => (
                            <div
                                key={`${location.latitude}-${location.longitude}-${index}`}
                                className={styles.resultItem}
                                onClick={() => handleSelectLocation(location)}
                            >
                                <div className={styles.resultName}>
                                    📍 {location.name}
                                </div>
                                <div className={styles.resultDetails}>
                                    {location.state && `${location.state}, `}
                                    {location.country}
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className={styles.noResults}>
                            No locations found. Try a different search.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

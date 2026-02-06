from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.schemas import LocationSearch, FavoriteLocation, AddFavoriteRequest
from app.models.models import Location, UserFavorite
from app.services.weather_service import weather_service

router = APIRouter(prefix="/api/locations", tags=["locations"])


@router.get("/search", response_model=List[LocationSearch])
async def search_locations(
    q: str = Query(..., description="Search query", min_length=2)
):
    """Search for locations by name"""
    
    locations = await weather_service.search_location(q)
    
    if not locations:
        return []
    
    return locations


@router.get("/favorites", response_model=List[FavoriteLocation])
async def get_favorites(
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get user's favorite locations"""
    
    favorites = db.query(UserFavorite).filter(
        UserFavorite.user_id == user_id
    ).join(Location).all()
    
    return [
        FavoriteLocation(
            id=fav.id,
            location_id=fav.location_id,
            location_name=fav.location.name,
            country=fav.location.country,
            latitude=fav.location.latitude,
            longitude=fav.location.longitude,
            created_at=fav.created_at
        )
        for fav in favorites
    ]


@router.post("/favorites", response_model=FavoriteLocation)
async def add_favorite(
    request: AddFavoriteRequest,
    db: Session = Depends(get_db)
):
    """Add a location to favorites"""
    
    # Find or create location
    location = db.query(Location).filter(
        Location.latitude == request.latitude,
        Location.longitude == request.longitude
    ).first()
    
    if not location:
        location = Location(
            name=request.location_name,
            country=request.country,
            state=request.state,
            latitude=request.latitude,
            longitude=request.longitude
        )
        db.add(location)
        db.commit()
        db.refresh(location)
    
    # Check if already favorited
    existing = db.query(UserFavorite).filter(
        UserFavorite.user_id == request.user_id,
        UserFavorite.location_id == location.id
    ).first()
    
    if existing:
        return FavoriteLocation(
            id=existing.id,
            location_id=existing.location_id,
            location_name=location.name,
            country=location.country,
            latitude=location.latitude,
            longitude=location.longitude,
            created_at=existing.created_at
        )
    
    # Create favorite
    favorite = UserFavorite(
        user_id=request.user_id,
        location_id=location.id
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    return FavoriteLocation(
        id=favorite.id,
        location_id=favorite.location_id,
        location_name=location.name,
        country=location.country,
        latitude=location.latitude,
        longitude=location.longitude,
        created_at=favorite.created_at
    )


@router.delete("/favorites/{favorite_id}")
async def delete_favorite(
    favorite_id: int,
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Delete a favorite location"""
    
    favorite = db.query(UserFavorite).filter(
        UserFavorite.id == favorite_id,
        UserFavorite.user_id == user_id
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "Favorite deleted successfully"}

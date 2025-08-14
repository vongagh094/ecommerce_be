from typing import List
from fastapi import HTTPException
from datetime import datetime
from app.schemas.AuctionDTO import AuctionCreateDTO, AuctionResponseDTO
from app.db.repositories.auction_repository import AuctionRepository
from app.features.property.repositories.property_repository import PropertyRepository
import logging

logger = logging.getLogger(__name__)

class AuctionService:
    def __init__(self, auction_repository: AuctionRepository, property_repository: PropertyRepository):
        self.auction_repository = auction_repository
        self.property_repository = property_repository

    def get_auctions_by_property(self, property_id: int) -> List[AuctionResponseDTO]:
        try:
            auctions = self.auction_repository.get_auctions_by_property(property_id)
            return [AuctionResponseDTO.model_validate(auction) for auction in auctions]
        except Exception as e:
            logger.error(f"Error getting auctions for property {property_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

    def create_auction(self, data: AuctionCreateDTO) -> AuctionResponseDTO:
        try:
            # Kiểm tra property_id
            property = self.property_repository.get_by_id(data.property_id)
            if not property:
                raise HTTPException(status_code=422, detail={"detail": "Property not found"})

            # Kiểm tra hợp lệ
            valid_objectives = ["HIGHEST_TOTAL", "HIGHEST_PER_NIGHT", "HYBRID"]
            if data.objective not in valid_objectives:
                raise HTTPException(status_code=422, detail={"detail": f"Invalid objective. Must be one of {valid_objectives}"})

            if data.start_date > data.end_date:
                raise HTTPException(status_code=422, detail={"detail": "End date must be after start date"})

            try:
                datetime.strptime(data.auction_start_time, "%H:%M")
                datetime.strptime(data.auction_end_time, "%H:%M")
            except ValueError:
                raise HTTPException(status_code=422, detail={"detail": "Invalid time format. Use HH:MM"})

            auction = self.auction_repository.create_auction(data)
            return AuctionResponseDTO.model_validate(auction)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error creating auction: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

    def delete_auction(self, auction_id: str) -> bool:
        try:
            success = self.auction_repository.delete_auction(auction_id)
            if not success:
                raise HTTPException(status_code=404, detail={"detail": "Auction not found"})
            return True
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error deleting auction {auction_id}: {str(e)}")
            raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})
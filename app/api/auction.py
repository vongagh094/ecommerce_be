from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.sessions.session import get_db_session
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.services.auction_service import AuctionService
from app.schemas.AuctionDTO import AuctionCreateDTO, AuctionResponseDTO,AuctionStatusUpdateResponse

router = APIRouter()

@router.get("/property/{property_id}", response_model=List[AuctionResponseDTO], operation_id="getAuctionsByProperty")
@inject
def get_auctions_by_property(
    property_id: int,
    db: Session = Depends(get_db_session),
    auction_service: AuctionService = Depends(Provide[Container.auction_service])
):
    return auction_service.get_auctions_by_property(property_id)

@router.post("/create", response_model=AuctionResponseDTO, operation_id="createAuction")
@inject
def create_auction(
    data: AuctionCreateDTO,
    db: Session = Depends(get_db_session),
    auction_service: AuctionService = Depends(Provide[Container.auction_service])
):
    return auction_service.create_auction(data)

@router.delete("/delete/{auction_id}", operation_id="deleteAuction")
@inject
def delete_auction(
    auction_id: str,
    db: Session = Depends(get_db_session),
    auction_service: AuctionService = Depends(Provide[Container.auction_service])
):
    success = auction_service.delete_auction(auction_id)
    return {"message": "Auction deleted successfully"} if success else {"message": "Auction not found"}

@router.put("/update/status/{auction_id}", response_model=AuctionStatusUpdateResponse, operation_id="updateAuction")
@inject
def update_auction  (
        auction_id: str,
        status: str,
        auction_service: AuctionService = Depends(Provide[Container.auction_service])
):
    return auction_service.update_status_auction(auction_id, status)

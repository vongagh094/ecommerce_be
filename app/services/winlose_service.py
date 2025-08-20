# 📁 FILE: app/services/win_lose_service.py

from typing import Dict, Optional, List
from datetime import timedelta
from app.db.repositories.bid_repository import BidRepository
from app.db.repositories.auction_repository import AuctionRepository
from app.db.models.Bid import Bids
from app.db.models.calendar_availability import CalendarAvailability
import logging

logger = logging.getLogger(__name__)


class WinLoseService:
    def __init__(self, bid_repository: BidRepository, auction_repository: AuctionRepository):
        self.bid_repository = bid_repository
        self.auction_repository = auction_repository

    def get_user_win_lose_status(self, user_id: int, auction_id: str) -> Dict:
        """
        Lấy win-lose status của user trong auction
        """
        try:
            # 1. Lấy bid hiện tại của user
            current_bid = self._get_user_active_bid(user_id, auction_id)

            if not current_bid:
                return {
                    "success": True,
                    "has_bid": False,
                    "message": "No active bid found"
                }

            # 2. Lấy property_id từ auction
            auction = self.auction_repository.get_auction_by_id(auction_id)
            if not auction:
                raise ValueError("Auction not found")

            # 3. Tính toán win-lose analysis
            analysis_result = self._calculate_win_lose_analysis(current_bid, auction.property_id)

            return {
                "success": True,
                "has_bid": True,
                **analysis_result
            }

        except Exception as e:
            logger.error(f"Error getting win-lose status for user {user_id}, auction {auction_id}: {e}")
            return {
                "success": False,
                "has_bid": False,
                "message": f"Error: {str(e)}"
            }

    def _get_user_active_bid(self, user_id: int, auction_id: str) -> Optional[Bids]:
        """
        Lấy bid active hiện tại của user trong auction
        """
        try:
            return self.bid_repository.db.query(Bids).filter(
                Bids.user_id == user_id,
                Bids.auction_id == auction_id,
                Bids.status == 'ACTIVE'
            ).first()
        except Exception as e:
            logger.error(f"Error getting user active bid: {e}")
            return None

    def _calculate_win_lose_analysis(self, bid: Bids, property_id: int) -> Dict:
        """
        Tính toán win-lose analysis cho một bid
        """
        try:
            # Tính price per day
            nights = (bid.check_out - bid.check_in).days
            bid_price_per_day = float(bid.price_per_night) if bid.price_per_night else \
                float(bid.total_amount) / max(1, nights)

            # Lấy danh sách ngày trong khoảng bid
            dates_in_range = self._get_dates_in_range(bid.check_in, bid.check_out)

            # So sánh với calendar cho từng ngày
            daily_results = {}
            win_days = 0
            total_days = len(dates_in_range)

            for date in dates_in_range:
                day_analysis = self._analyze_day(date, bid_price_per_day, property_id)
                daily_results[date.isoformat()] = day_analysis

                if day_analysis["status"] == "WIN":
                    win_days += 1

            # Tính summary
            win_rate = (win_days / total_days * 100) if total_days > 0 else 0

            return {
                "bid_info": {
                    "bid_id": str(bid.id),
                    "total_amount": float(bid.total_amount),
                    "price_per_day": bid_price_per_day,
                    "check_in": bid.check_in.isoformat(),
                    "check_out": bid.check_out.isoformat(),
                    "nights": total_days
                },
                "summary": {
                    "total_days": total_days,
                    "win_days": win_days,
                    "lose_days": total_days - win_days,
                    "win_rate": round(win_rate, 1),
                    "overall_status": self._determine_overall_status(win_rate)
                },
                "daily_results": daily_results
            }

        except Exception as e:
            logger.error(f"Error calculating win-lose analysis: {e}")
            raise

    def _analyze_day(self, date, bid_price_per_day: float, property_id: int) -> Dict:
        """
        Phân tích win-lose cho một ngày cụ thể
        """
        try:
            # Lấy market price từ calendar
            calendar_entry = self.bid_repository.db.query(CalendarAvailability).filter(
                CalendarAvailability.property_id == property_id,
                CalendarAvailability.date == date
            ).first()

            market_price = float(
                calendar_entry.price_amount) if calendar_entry and calendar_entry.price_amount else None

            if market_price is not None:
                if bid_price_per_day >= market_price:
                    status = "WIN"
                else:
                    status = "LOSE"
                difference = bid_price_per_day - market_price
                difference_percentage = (difference / market_price * 100) if market_price > 0 else 0
            else:
                status = "NO_DATA"
                difference = None
                difference_percentage = None

            return {
                "bid_price": bid_price_per_day,
                "market_price": market_price,
                "status": status,
                "difference": round(difference, 2) if difference is not None else None,
                "difference_percentage": round(difference_percentage, 2) if difference_percentage is not None else None
            }

        except Exception as e:
            logger.error(f"Error analyzing day {date}: {e}")
            return {
                "bid_price": bid_price_per_day,
                "market_price": None,
                "status": "ERROR",
                "difference": None,
                "difference_percentage": None
            }

    def _get_dates_in_range(self, check_in, check_out) -> List:
        """
        Lấy danh sách ngày từ check_in đến check_out (không bao gồm check_out)
        """
        dates = []
        current_date = check_in
        while current_date < check_out:
            dates.append(current_date)
            current_date += timedelta(days=1)
        return dates

    def _determine_overall_status(self, win_rate: float) -> str:
        """
        Xác định overall status dựa trên win rate
        """
        if win_rate > 50:
            return "WINNING"
        elif win_rate < 50:
            return "LOSING"
        else:
            return "TIE"

    def get_bid_performance_insights(self, user_id: int, auction_id: str) -> Dict:
        """
        Lấy performance insights chi tiết (có thể mở rộng sau)
        """
        try:
            basic_analysis = self.get_user_win_lose_status(user_id, auction_id)

            if not basic_analysis.get("has_bid"):
                return basic_analysis

            # Có thể thêm more insights ở đây
            insights = {
                "performance_rating": self._get_performance_rating(basic_analysis["summary"]["win_rate"]),
                "recommendations": self._get_recommendations(basic_analysis["summary"])
            }

            return {
                **basic_analysis,
                "insights": insights
            }

        except Exception as e:
            logger.error(f"Error getting performance insights: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def _get_performance_rating(self, win_rate: float) -> str:
        """
        Đánh giá performance dựa trên win rate
        """
        if win_rate >= 80:
            return "EXCELLENT"
        elif win_rate >= 60:
            return "GOOD"
        elif win_rate >= 40:
            return "AVERAGE"
        else:
            return "POOR"

    def _get_recommendations(self, summary: Dict) -> List[str]:
        """
        Tạo recommendations dựa trên analysis
        """
        recommendations = []
        win_rate = summary.get("win_rate", 0)

        if win_rate >= 80:
            recommendations.append("Excellent bidding strategy! Keep it up.")
        elif win_rate >= 60:
            recommendations.append("Good performance. Consider minor optimizations.")
        elif win_rate >= 40:
            recommendations.append("Average performance. Consider adjusting bid amount.")
        else:
            recommendations.append("Consider lowering bid amount for better competitiveness.")

        if summary.get("lose_days", 0) > summary.get("win_days", 0):
            recommendations.append("You're losing on most days. Review market prices.")

        return recommendations
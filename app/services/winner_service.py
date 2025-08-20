from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict
from pydantic import BaseModel
from app.db.repositories.bid_repository import BidRepository
from app.db.repositories.auction_repository import AuctionRepository


class DailyWinner(BaseModel):
    """Pydantic model cho daily winner - chỉ trả về thông tin winner từng ngày"""
    date: str
    user_id: int
    price_per_day: float
    total_amount: float

    class Config:
        from_attributes = True


class WinnerService:
    def __init__(self, bid_repository: BidRepository, auction_repository: AuctionRepository):
        self.bid_repository = bid_repository
        self.auction_repository = auction_repository

    def calculate_winners(self, auction_id: str) -> List[DailyWinner]:
        """
        Tính toán người chiến thắng cho từng ngày.
        Chỉ trả về winners, KHÔNG tạo booking.
        """
        # 1. Lấy auction info
        auction = self.auction_repository.get_auction_by_id(auction_id)
        if not auction:
            raise ValueError("Auction not found")

        # 2. Lấy active bids
        bids = self.bid_repository.get_active_bids_by_auction(auction_id)
        if not bids:
            return []

        # 3. Duyệt từng ngày, tìm winner cho từng ngày
        winners = []
        current_date = auction.start_date

        while current_date <= auction.end_date:
            winner = self._find_winner_for_date(current_date, bids)
            if winner:
                winners.append(DailyWinner(
                    date=current_date.strftime('%Y-%m-%d'),
                    user_id=winner["user_id"],
                    price_per_day=winner["price_per_day"],
                    total_amount=winner["total_amount"]
                ))
            current_date += timedelta(days=1)

        return winners

    def calculate_booking_periods(self, auction_id: str) -> List[Dict]:
        """
        Convert daily winners thành booking periods liên tục.

        Returns:
        [
            {
                "auction_id": "auction_123",
                "check_in_win": "2025-08-25",
                "check_out_win": "2025-08-28",
                "amount": 135.0,
                "user_id": 1
            }
        ]
        """
        # 1. Lấy daily winners
        daily_winners = self.calculate_winners(auction_id)

        if not daily_winners:
            return []

        # 2. Group by user_id
        user_winning_dates = defaultdict(list)

        for winner in daily_winners:
            user_winning_dates[winner.user_id].append({
                'date': winner.date,
                'price_per_day': winner.price_per_day
            })

        # 3. Sort dates for each user
        for user_id in user_winning_dates:
            user_winning_dates[user_id].sort(key=lambda x: x['date'])

        # 4. Create booking periods for each user
        booking_periods = []

        for user_id, winning_dates in user_winning_dates.items():
            user_periods = self._create_consecutive_periods(user_id, winning_dates)

            for period in user_periods:
                booking_periods.append({
                    "auction_id": auction_id,
                    "check_in_win": period['check_in'],
                    "check_out_win": period['check_out'],
                    "amount": period['total_amount'],
                    "user_id": user_id
                })

        return booking_periods

    def _create_consecutive_periods(self, user_id: int, winning_dates: List[Dict]) -> List[Dict]:
        """Tạo các periods liên tục từ list winning dates"""
        if not winning_dates:
            return []

        periods = []
        current_period = {
            'dates': [winning_dates[0]],
            'check_in': winning_dates[0]['date']
        }

        # Group consecutive dates
        for i in range(1, len(winning_dates)):
            current_date = winning_dates[i]['date']
            prev_date = winning_dates[i - 1]['date']

            # Check if consecutive (1 day difference)
            current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            prev_dt = datetime.strptime(prev_date, '%Y-%m-%d')

            if (current_dt - prev_dt).days == 1:
                # Consecutive - add to current period
                current_period['dates'].append(winning_dates[i])
            else:
                # Not consecutive - finalize current period and start new
                periods.append(self._finalize_period(current_period))
                current_period = {
                    'dates': [winning_dates[i]],
                    'check_in': current_date
                }

        # Don't forget the last period
        periods.append(self._finalize_period(current_period))

        return periods

    def _finalize_period(self, period: Dict) -> Dict:
        """Hoàn thiện thông tin cho booking period"""
        dates = period['dates']
        check_in = period['check_in']

        # Check-out = last date + 1 day
        last_date = dates[-1]['date']
        check_out_dt = datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1)
        check_out = check_out_dt.strftime('%Y-%m-%d')

        # Total amount = sum of price_per_day for each winning day
        total_amount = sum(d['price_per_day'] for d in dates)

        return {
            'check_in': check_in,
            'check_out': check_out,
            'total_amount': total_amount,
            'nights': len(dates)
        }
    def _find_winner_for_date(self, date: datetime, bids) -> Dict:
        """Tìm winner cho 1 ngày cụ thể - người bid giá cao nhất cho ngày đó."""
        valid_bids = []

        for bid in bids:
            # Convert to date if datetime
            check_in = bid.check_in.date() if hasattr(bid.check_in, 'date') else bid.check_in
            check_out = bid.check_out.date() if hasattr(bid.check_out, 'date') else bid.check_out
            target_date = date.date() if hasattr(date, 'date') else date

            # Check if bid covers this date
            if check_in <= target_date < check_out:  # Note: < check_out vì checkout không tính

                # Tính price per day
                nights = (check_out - check_in).days
                total_days = nights  # Số ngày = số đêm

                if total_days > 0:
                    price_per_day = float(bid.total_amount) / total_days
                else:
                    continue  # Skip invalid bids

                valid_bids.append({
                    "user_id": bid.user_id,
                    "price_per_day": price_per_day,
                    "total_amount": float(bid.total_amount)
                })

        if not valid_bids:
            return None

        # Tìm winner theo price_per_day cao nhất
        return max(valid_bids, key=lambda x: x["price_per_day"])
    #
    # def get_winners_summary(self, auction_id: str) -> Dict:
    #     """
    #     Lấy summary của winners - ai thắng bao nhiêu ngày, tổng tiền là bao nhiêu.
    #     """
    #     winners = self.calculate_winners(auction_id)
    #
    #     if not winners:
    #         return {
    #             "total_days": 0,
    #             "winners_count": 0,
    #             "user_summaries": {}
    #         }
    #
    #     # Group by user
    #     user_summaries = defaultdict(lambda: {
    #         "days_won": 0,
    #         "total_amount": 0.0,
    #         "winning_dates": []
    #     })
    #
    #     for winner in winners:
    #         user_id = winner.user_id
    #         user_summaries[user_id]["days_won"] += 1
    #         user_summaries[user_id]["total_amount"] += winner.price_per_day
    #         user_summaries[user_id]["winning_dates"].append({
    #             "date": winner.date,
    #             "price_per_day": winner.price_per_day
    #         })
    #
    #     return {
    #         "total_days": len(winners),
    #         "winners_count": len(user_summaries),
    #         "user_summaries": dict(user_summaries)
    #     }
    #
    #
    # def get_winner_for_specific_date(self, auction_id: str, target_date: str) -> DailyWinner:
    #     """
    #     Lấy winner cho 1 ngày cụ thể.
    #
    #     Args:
    #         auction_id: ID của auction
    #         target_date: Ngày cần check (format: 'YYYY-MM-DD')
    #
    #     Returns:
    #         DailyWinner object hoặc None nếu không có winner
    #     """
    #     # Parse target date
    #     try:
    #         date_obj = datetime.strptime(target_date, '%Y-%m-%d')
    #     except ValueError:
    #         raise ValueError("Invalid date format. Use 'YYYY-MM-DD'")
    #
    #     # Lấy auction và bids
    #     auction = self.auction_repository.get_auction_by_id(auction_id)
    #     if not auction:
    #         raise ValueError("Auction not found")
    #
    #     # Check if date is within auction period
    #     if not (auction.start_date <= date_obj.date() <= auction.end_date):
    #         return None
    #
    #     bids = self.bid_repository.get_active_bids_by_auction(auction_id)
    #     if not bids:
    #         return None
    #
    #     # Find winner for this specific date
    #     winner = self._find_winner_for_date(date_obj, bids)
    #     if not winner:
    #         return None
    #
    #     return DailyWinner(
    #         date=target_date,
    #         user_id=winner["user_id"],
    #         price_per_day=winner["price_per_day"],
    #         total_amount=winner["total_amount"]
    #     )
    #
    # def get_user_winning_days(self, auction_id: str, user_id: int) -> List[DailyWinner]:
    #     """
    #     Lấy tất cả những ngày mà user này thắng trong auction.
    #     """
    #     all_winners = self.calculate_winners(auction_id)
    #     return [winner for winner in all_winners if winner.user_id == user_id]
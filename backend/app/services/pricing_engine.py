"""Rules-based Dynamic Pricing Engine for hotel rooms.

Calculates nightly rates using four pricing factors:
1. Occupancy rate
2. Lead time (days until check-in)
3. Day of week (weekend premiums)
4. Local demand events
"""

from datetime import date
from typing import Optional

from app.schemas.schemas import PricingBreakdown


class PricingEngineInterface:
    def calculate_nightly_price(
        self,
        base_price: float,
        target_date: date,
        booked_rooms: int,
        total_rooms: int,
        booking_date: date,
        event_multiplier: float = 1.0,
        event_name: Optional[str] = None,
    ) -> PricingBreakdown:
        raise NotImplementedError


class DynamicPricingEngine(PricingEngineInterface):
    """Production pricing engine with floor/ceiling caps."""

    # Floor and Ceiling caps relative to base_price
    MIN_PRICE_FLOOR_FACTOR: float = 0.50
    MAX_PRICE_CEILING_FACTOR: float = 3.00

    def get_occupancy_multiplier(
        self, occupancy_rate: float,
    ) -> float:
        """Occupancy-based multiplier tiers."""
        if occupancy_rate < 0.30:
            return 0.85  # Low occupancy discount
        elif occupancy_rate < 0.60:
            return 1.00  # Baseline
        elif occupancy_rate < 0.80:
            return 1.20  # Strong demand
        elif occupancy_rate < 0.95:
            return 1.40  # High demand
        else:
            return 1.65  # Near capacity premium

    def get_lead_time_multiplier(
        self, days_to_checkin: int,
    ) -> float:
        """Lead-time multiplier tiers."""
        if days_to_checkin <= 2:
            return 1.25  # Last-minute premium
        elif days_to_checkin <= 7:
            return 1.10  # Short-notice premium
        elif days_to_checkin <= 30:
            return 1.00  # Standard window
        elif days_to_checkin <= 60:
            return 0.92  # Early bird discount
        else:
            return 0.85  # Advance purchase discount

    def get_weekend_multiplier(
        self, target_date: date,
    ) -> tuple[bool, float]:
        """Fri/Sat get weekend premiums; Sun a slight bump."""
        weekday = target_date.weekday()
        if weekday in (4, 5):  # Fri, Sat
            return True, 1.20
        elif weekday == 6:  # Sun
            return False, 1.05
        return False, 1.00

    def calculate_nightly_price(
        self,
        base_price: float,
        target_date: date,
        booked_rooms: int,
        total_rooms: int,
        booking_date: date,
        event_multiplier: float = 1.0,
        event_name: Optional[str] = None,
    ) -> PricingBreakdown:
        # 1. Occupancy
        occupancy_rate = min(
            max(booked_rooms / max(total_rooms, 1), 0.0), 1.0,
        )
        m_occ = self.get_occupancy_multiplier(occupancy_rate)

        # 2. Lead time
        days_to_checkin = max(
            (target_date - booking_date).days, 0,
        )
        m_lead = self.get_lead_time_multiplier(days_to_checkin)

        # 3. Weekend / day of week
        is_weekend, m_weekend = self.get_weekend_multiplier(
            target_date,
        )

        # 4. Demand events
        m_event = max(event_multiplier, 1.0)

        # 5. Combined multiplier with floor/ceiling caps
        total_multiplier = m_occ * m_lead * m_weekend * m_event
        raw_price = base_price * total_multiplier

        min_allowed = base_price * self.MIN_PRICE_FLOOR_FACTOR
        max_allowed = base_price * self.MAX_PRICE_CEILING_FACTOR

        final_price = round(
            min(max(raw_price, min_allowed), max_allowed), 2,
        )

        # Human-readable explanation for tooltip UI
        factors = []
        if m_occ != 1.0:
            factors.append(
                f"Occupancy ({occupancy_rate * 100:.0f}%"
                f" -> {m_occ}x)"
            )
        if m_lead != 1.0:
            factors.append(
                f"Lead time ({days_to_checkin}d -> {m_lead}x)"
            )
        if m_weekend != 1.0:
            factors.append(
                f"Weekend premium ({m_weekend}x)"
            )
        if m_event > 1.0:
            event_label = event_name or "Special Event"
            factors.append(
                f"Event: {event_label} ({m_event}x)"
            )

        explanation = (
            ", ".join(factors)
            if factors
            else "Standard base rate applied."
        )

        return PricingBreakdown(
            date=target_date,
            base_price=base_price,
            final_price=final_price,
            occupancy_rate=round(occupancy_rate, 4),
            occupancy_multiplier=m_occ,
            days_to_checkin=days_to_checkin,
            lead_time_multiplier=m_lead,
            is_weekend=is_weekend,
            weekend_multiplier=m_weekend,
            demand_event_name=(
                event_name if m_event > 1.0 else None
            ),
            demand_event_multiplier=m_event,
            total_multiplier=round(total_multiplier, 4),
            explanation=explanation,
        )


# Singleton default engine
pricing_engine = DynamicPricingEngine()

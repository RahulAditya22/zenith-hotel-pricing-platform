from datetime import date

import pytest

from app.services.pricing_engine import DynamicPricingEngine


@pytest.fixture
def engine() -> DynamicPricingEngine:
    return DynamicPricingEngine()


def test_base_price_standard_day(engine: DynamicPricingEngine):
    # Mon check-in, 15 days out, 40% occupancy, no events
    target_date = date(2026, 10, 12)  # Monday
    booking_date = date(2026, 9, 27)  # 15 days prior

    breakdown = engine.calculate_nightly_price(
        base_price=100.0,
        target_date=target_date,
        booked_rooms=4,
        total_rooms=10,  # 40% occupancy -> 1.0x
        booking_date=booking_date,  # 15 days lead time -> 1.0x
    )

    assert breakdown.base_price == 100.0
    assert breakdown.occupancy_rate == 0.4
    assert breakdown.occupancy_multiplier == 1.0
    assert breakdown.lead_time_multiplier == 1.0
    assert breakdown.weekend_multiplier == 1.0
    assert breakdown.final_price == 100.0


def test_high_occupancy_and_weekend_surge(engine: DynamicPricingEngine):
    # Friday check-in, 90% occupancy, 5 days lead time
    target_date = date(2026, 10, 16)  # Friday
    booking_date = date(2026, 10, 11)  # 5 days lead time (1.10x)

    breakdown = engine.calculate_nightly_price(
        base_price=200.0,
        target_date=target_date,
        booked_rooms=9,
        total_rooms=10,  # 90% occupancy -> 1.40x
        booking_date=booking_date,
    )

    # m_occ = 1.40, m_lead = 1.10, m_weekend = 1.20
    # total = 1.40 * 1.10 * 1.20 = 1.848
    # raw_price = 200 * 1.848 = 369.6
    assert breakdown.occupancy_multiplier == 1.40
    assert breakdown.lead_time_multiplier == 1.10
    assert breakdown.is_weekend is True
    assert breakdown.weekend_multiplier == 1.20
    assert breakdown.final_price == round(200.0 * (1.40 * 1.10 * 1.20), 2)


def test_demand_event_multiplier(engine: DynamicPricingEngine):
    target_date = date(2026, 10, 15)  # Thursday
    booking_date = date(2026, 10, 1)  # 14 days out (1.0x)

    breakdown = engine.calculate_nightly_price(
        base_price=150.0,
        target_date=target_date,
        booked_rooms=2,
        total_rooms=10,  # 20% occupancy -> 0.85x
        booking_date=booking_date,
        event_multiplier=1.5,
        event_name="Tech Conference",
    )

    # m_occ = 0.85, m_lead = 1.0, m_weekend = 1.0, m_event = 1.5
    # total = 0.85 * 1.5 = 1.275
    # expected = 150 * 1.275 = 191.25
    assert breakdown.demand_event_multiplier == 1.5
    assert breakdown.demand_event_name == "Tech Conference"
    assert breakdown.final_price == 191.25


def test_price_floor_and_ceiling(engine: DynamicPricingEngine):
    target_date = date(2026, 10, 14)
    booking_date = date(2026, 7, 1)  # 105 days out -> 0.85x

    # Test Floor (low occupancy + early lead)
    breakdown_floor = engine.calculate_nightly_price(
        base_price=100.0,
        target_date=target_date,
        booked_rooms=0,  # 0% -> 0.85x
        total_rooms=10,
        booking_date=booking_date,
    )
    # 0.85 * 0.85 = 0.7225 -> 72.25. (Above floor 50.0)
    assert breakdown_floor.final_price >= 50.0

    # Test Ceiling cap
    breakdown_ceiling = engine.calculate_nightly_price(
        base_price=100.0,
        target_date=date(2026, 10, 16),  # Friday weekend 1.20x
        booked_rooms=10,  # 100% -> 1.65x
        total_rooms=10,
        booking_date=date(2026, 10, 15),  # 1 day out -> 1.25x
        event_multiplier=2.5,  # Event 2.5x
    )
    # 1.65 * 1.25 * 1.20 * 2.5 = 6.1875 (exceeds max ceiling 3.00x)
    assert breakdown_ceiling.final_price == 300.00

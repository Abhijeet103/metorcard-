import pytest
from src.model import MetroCard
from src.service import MetroService

metroService = MetroService()

@pytest.fixture(autouse=True)
def reset():
    global metroService
    metroService = MetroService()

@pytest.fixture
def rate():
    return {
        "ADULT": 200,
        "SENIOR_CITIZEN": 100,
        "KID": 50
    }

@pytest.fixture
def station_central():
    return metroService.stations['CENTRAL']

@pytest.fixture
def station_airport():
    return metroService.stations['AIRPORT']

@pytest.fixture
def new_card():
    def _create(mid="MC1", balance=500):
        card = MetroCard(mid, balance)
        metroService.metroCard[mid] = card
        return card
    return _create

def test_balance():
    metroService.create_card("MC123", 500)
    assert "MC123" in metroService.metroCard
    assert metroService.metroCard["MC123"].balance == 500

def test_recharge_card(new_card, station_central):
    card = new_card("MC2", 100)
    metroService.rechargeCard(card, 200, "CENTRAL")

    assert card.balance == 300
    # Assuming add_ammount increments by 4 in this context (might be logging)
    assert station_central.total_amount == 4

def test_check_in_single_trip(new_card, rate, station_central):
    card = new_card(mid="MC123", balance=500)

    metroService.check_in("MC123", "ADULT", "CENTRAL")

    assert card.balance == 300
    assert station_central.total_amount == 200
    assert station_central.passenger_history["ADULT"] == 1

def test_check_in_round_trip(new_card, station_airport, station_central):
    card = new_card(mid="MC1", balance=500)

    metroService.check_in("MC1", "ADULT", "AIRPORT")
    assert card.src == "AIRPORT"

    metroService.check_in("MC1", "ADULT", "CENTRAL")

    assert card.balance == 200
    assert station_central.discount == 100
    assert station_central.passenger_history["ADULT"] == 1
    assert card.src is None

def test_check_in_three_trips_with_round_trip(new_card, station_central, station_airport):
    card = new_card(mid="MC5", balance=1000)

    metroService.check_in("MC5", "ADULT", "AIRPORT")
    assert card.src == "AIRPORT"
    assert station_airport.total_amount == 200
    assert station_airport.passenger_history["ADULT"] == 1

    metroService.check_in("MC5", "ADULT", "CENTRAL")

    assert station_central.discount == 100
    assert station_central.total_amount == 100
    assert station_central.passenger_history["ADULT"] == 1
    assert card.src is None

    metroService.check_in("MC5", "ADULT", "CENTRAL")
    assert card.src == "CENTRAL"
    assert station_central.total_amount == 300
    assert station_central.passenger_history["ADULT"] == 2
    assert card.balance == 500

def test_summary_multiple_types(new_card):
    new_card("MC1", 300)
    new_card("MC2", 300)

    metroService.check_in("MC1", "KID", "CENTRAL")
    metroService.check_in("MC2", "ADULT", "CENTRAL")

    result = metroService.summary()

    expected = (
        "TOTAL_COLLECTION CENTRAL 250 0\n"
        "PASSENGER_TYPE_SUMMARY\n"
        "ADULT 1\n"
        "KID 1\n"
        "TOTAL_COLLECTION AIRPORT 0 0\n"
        "PASSENGER_TYPE_SUMMARY"
    )

    assert result.strip() == expected.strip()

def test_summary_passenger_order_sorted(new_card):
    new_card("MC1", 300)
    new_card("MC2", 300)
    new_card("MC3", 300)

    metroService.check_in("MC1", "KID", "CENTRAL")
    metroService.check_in("MC2", "ADULT", "CENTRAL")
    metroService.check_in("MC3", "SENIOR_CITIZEN", "CENTRAL")

    result = metroService.summary()

    lines = result.splitlines()
    start_index = lines.index("PASSENGER_TYPE_SUMMARY")
    passenger_lines = []

    for line in lines[start_index + 1:]:
        if line.startswith("TOTAL_COLLECTION"):
            break
        passenger_lines.append(line)

    passenger_types = [line.split()[0] for line in passenger_lines]

    assert passenger_types == sorted(passenger_types)

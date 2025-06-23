from .model import MetroCard, Station, Fare

class MetroService:
    def __init__(self):
        self.metroCard = {}
        self.stations = {
            "CENTRAL": Station("CENTRAL"),
            "AIRPORT": Station("AIRPORT")
        }

    def create_card(self, mid, amount):
        self.metroCard[mid] = MetroCard(mid, int(amount))

    def rechargeCard(self, card, amount, station_name):
        card.add_balance(amount)
        station = self.stations[station_name]
        cashback = amount * 2 / 100
        station.add_amount(cashback)

    def check_in(self, mid, passenger_type, src):
        card = self.metroCard[mid]
        round_trip = (
            (card.src == "AIRPORT" and src == "CENTRAL") or
            (card.src == "CENTRAL" and src == "AIRPORT")
        )

        fare = Fare.get_fare(passenger_type, round_trip)
        station = self.stations[src]

        if card.balance < fare:
            self.rechargeCard(card, fare - card.balance, src)

        card.add_balance(-fare)

        if round_trip:
            card.update_src(None)
            station.add_discount(fare)
        else:
            card.update_src(src)

        station.add_amount(fare)
        station.add_passenger(passenger_type)

    def summary(self):
        output = []
        for station_name in ['CENTRAL', 'AIRPORT']:
            station = self.stations[station_name]

            output.append(
                f"TOTAL_COLLECTION {station_name} {int(station.total_amount)} {int(station.discount)}"
            )
            output.append("PASSENGER_TYPE_SUMMARY")

            for passenger_type, count in sorted(station.passenger_history.items()):
                output.append(f"{passenger_type} {count}")

        return "\n".join(output)

from data_models import KoronaData


def calculate_amount(korona_data: KoronaData, amount) -> KoronaData:
    data = korona_data
    int_amount = int(amount)
    data.sending_amount = round(data.rate * int_amount, 2)
    data.receiving_amount = int_amount
    return data

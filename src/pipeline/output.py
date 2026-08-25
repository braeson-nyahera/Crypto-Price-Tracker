def output_terminal(data):
    if len(data) == 1:
        single_output = f"""
    ------------------------------------------------
    BINANCE CRYPTO DATA
    ------------------------------------------------
    symbol:             {data[0]['symbol']}
    Price USDT:         $ {data[0]['price']}
    USD/KES Rate:       {data[0]['USD/KES rates']}
    Approx. Price KES:  KSh {data[0]['Approx. Price KES']}
    --------------------------------------------------
    Source: Binance
    Status: SUCCESS
    --------------------------------------------------

        """
        print(single_output)

def output_json(data):
    output = data


def output_data(data, output_form):
    if output_form == "terminal":
        output_terminal(data)
    elif output_form == 'json':
        output_json(data)
    return data
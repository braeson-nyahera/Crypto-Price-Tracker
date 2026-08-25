import csv
import json
import os.path

def output_terminal(data, currency):
    if len(data) == 1:
        single_output = f"""
    ------------------------------------------------
    BINANCE CRYPTO DATA
    ------------------------------------------------
    symbol:             {data[0]['symbol']}
    Price USDT:         $ {data[0]['price']:,.2f}
    USD/{currency} Rate:       {data[0][f'USD/{currency} rates']}
    Approx. Price {currency}:  {currency} {data[0][F'Approx. Price {currency}']:,.2f}
    --------------------------------------------------
    Source: Binance
    Status: SUCCESS
    --------------------------------------------------

        """
        print(single_output)

    else:
        print(f"""
    --------------------------------------------------------------------
    SYMBOL       USDT PRICE              APPROXIMATE {currency} (rates = {data[0][f'USD/{currency} rates']})
    --------------------------------------------------------------------""")
        for value in data:
            print(f"    {value['symbol']:<10}   $ {value['price']:<20}  {currency} {value[f'Approx. Price {currency}']}")
        print(f"    --------------------------------------------------------------------")  

def output_json(data):
    with open("output.json", "w") as output_file:
        json.dump(data, output_file, indent=2)

    print(f"JSON file successfully created at: {os.path.curdir}/output.json")

def output_csv(data):
    fieldnames = data[0].keys()

    with open("output.csv", "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(data)

    print(f"CSV file successfully created at: {os.path.curdir}/output.csv")

def output_postgres(data):
    print(data)

def output_data(data, output_form, currency):
    if output_form == "terminal":
        output_terminal(data, currency)
    elif output_form == 'json':
        output_json(data)
    elif output_form == 'csv':
        output_csv(data)
    elif output_form == 'postgres':
        output_postgres(data)
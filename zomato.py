import requests
import json
import sys
from rich import print


HEADERS = {
    'Host': 'www.zomato.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.zomato.com/',
    'Content-Type': 'application/json'
}


GET_ORDERS_URL = "https://www.zomato.com/webroutes/user/orders?page="


def getOrders(cookies):
    print("Retrieving...")
    spent = 0
    s = requests.Session()
    current_page = 1
    num_of_orders = 0
    while True:
        URL = GET_ORDERS_URL+str(current_page).strip()

        r = s.get(URL, headers=HEADERS, cookies=cookies)
        resp = json.loads(r.text)
        total_pages = resp['sections']['SECTION_USER_ORDER_HISTORY']['totalPages']

        for order_id in resp['entities']['ORDER']:
            order = resp['entities']['ORDER'][order_id]
            if order['totalCost']:
                order_total = order['totalCost'][1:].replace(",", "")
                order_total = float(order_total)
            else:
                order_total = 0
            # print(order_total)
            num_of_orders += 1
            spent += order_total

        if current_page >= total_pages:
            print("Reached end of orders")
            break

        current_page += 1

    average_spent = spent//num_of_orders
    print()
    print(
        f"[green]Total money spent on zomato.com : [bold]INR {spent:,}[/bold][/green]")
    print(
        f"[green]Total number of orders placed : [bold]{num_of_orders:,}[/bold][/green]")
    print(
        f"[green]Average money spent on each order : [bold]INR {average_spent:,}[/bold][/green]")


def cookiesToDict():
    print("[green][+][/green] Getting cookies from [u]cookies.json[/u]")
    data = None
    cookies = {}
    try:
        with open("cookies.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("[red][-] [u]cookies.json[/u] not found in the path[/red]")
        print(str(e))
        return None

    try:
        for i in data:
            cookies[i['name']] = i['value']
    except Exception as e:
        print("[red][-] Cookies are not in proper format[/red]")
        print(str(e))
        return None

    return cookies


def checkLogin(cookies):
    # First check if logged in
    print("[green][+][/green] Checking if session is valid")
    r = requests.get(GET_ORDERS_URL, headers=HEADERS, cookies=cookies)
    resp = None
    try:
        resp = json.loads(r.text)
    except Exception as e:
        print("[red][-] Unexpected Response received[/red]")
        return False

    if resp['sections']["SECTION_USER_ORDER_HISTORY"]['count'] == 0:
        print("[red][-] Not logged in, or no Orders found[/red]")
        return False

    print("[green][+][/green] Session is valid")
    return True


if __name__ == "__main__":
    print("Started Script..:vampire:")
    cookies = cookiesToDict()
    if cookies is None:
        sys.exit()
    if checkLogin(cookies):
        getOrders(cookies)

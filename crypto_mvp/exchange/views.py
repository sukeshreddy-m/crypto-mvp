from django.shortcuts import render, redirect
import requests

# ---------------- Market Page ----------------
def market(request):
    query = request.GET.get('q', '').lower()
    vs_currency = request.GET.get('currency', 'usd').lower()

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        coins = response.json()
    except Exception as e:
        print("Error fetching data:", e)
        coins = []

    if query:
        coins = [c for c in coins if query in c['name'].lower() or query in c['symbol'].lower()]

    logged_in = request.session.get('logged_in', False)
    username = request.session.get('username', None)

    return render(request, "market.html", {
        "coins": coins,
        "query": query,
        "vs_currency": vs_currency.upper(),
        "logged_in": logged_in,
        "username": username
    })


# ---------------- Coin Detail ----------------
def coin_detail(request, coin_id):
    days = request.GET.get('days', '7')
    vs_currency = request.GET.get('currency', 'usd').lower()

    # ✅ Preserve login session info
    logged_in = request.session.get('logged_in', False)
    username = request.session.get('username', None)

    chart_url = f"https://api.coingecko.com/api/v3/coins/{coin_id.lower()}/market_chart"
    chart_params = {"vs_currency": vs_currency, "days": days}

    chart_data = {}
    try:
        chart_response = requests.get(chart_url, params=chart_params, timeout=10)
        chart_response.raise_for_status()
        chart_data = chart_response.json()
    except Exception as e:
        print("Chart API error:", e)

    meta_url = f"https://api.coingecko.com/api/v3/coins/{coin_id.lower()}"
    coin_meta = {}
    try:
        meta_response = requests.get(meta_url, timeout=10)
        meta_response.raise_for_status()
        coin_meta = meta_response.json()
    except Exception as e:
        print("Meta API error:", e)

    return render(request, "coin_detail.html", {
        "coin": coin_meta,
        "chart_data": chart_data,
        "days": days,
        "vs_currency": vs_currency.upper(),
        "logged_in": logged_in,   # ✅ Added
        "username": username      # ✅ Added
    })

# ---------------- Login / Logout ----------------
def login_view(request):
    message = ""
    show_register = request.GET.get('register', 'false').lower() == 'true'

    if show_register:
        message = "⚠️ Registration is currently unavailable. Please try again later."

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "Sukesh1710" and password == "Sukesh@2002":
            request.session['logged_in'] = True
            request.session['username'] = username
            return redirect('/market/')
        else:
            message = "❌ Invalid username or password."

    return render(request, "login.html", {"message": message, "register": show_register})


def logout_view(request):
    request.session.flush()
    return redirect('/market/')

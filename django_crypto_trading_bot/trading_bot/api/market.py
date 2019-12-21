from django_crypto_trading_bot.trading_bot.models import Market, Currency
from .client import get_client
from ccxt.base.exchange import Exchange


def get_or_create_market(response: dict, exchange_id: str) -> Market:
    """
    update or create a market based on the api json
    """
    base, create = Currency.objects.get_or_create(short=response["base"])
    quote, create = Currency.objects.get_or_create(short=response["quote"])

    try:
        market: Market = Market.objects.get(
            base=base, quote=quote, exchange=exchange_id
        )
        market.active = response["active"]
        market.precision_amount = response["precision"]["amount"]
        market.precision_price = response["precision"]["price"]
        market.limits_amount_min = response["limits"]["amount"]["min"]
        market.limits_amount_max = response["limits"]["amount"]["max"]
        market.limits_price_min = response["limits"]["price"]["min"]
        market.limits_price_max = response["limits"]["price"]["max"]
        market.save()
        return market

    except Market.DoesNotExist:
        return Market.objects.create(
            base=base,
            quote=quote,
            exchange=exchange_id,
            active=response["active"],
            precision_amount=response["precision"]["amount"],
            precision_price=response["precision"]["price"],
            limits_amount_min=response["limits"]["amount"]["min"],
            limits_amount_max=response["limits"]["amount"]["max"],
            limits_price_min=response["limits"]["price"]["min"],
            limits_price_max=response["limits"]["price"]["max"],
        )


def update_market(market: Market, exchange: Exchange = None) -> Market:
    """
    Update Market Order

    Keyword arguments:
    market -- market model
    exchange -- exchange client, preload all markets to reduce requests

    return -> Market, updated market
    """
    if not exchange:
        exchange = get_client(exchange_id=market.exchange)

    market_exchange: dict = exchange.market(market.symbol)
    return get_or_create_market(response=market_exchange, exchange_id=market.exchange)


def update_all_markets(exchange: Exchange):
    """
    Update all markets
    """
    for market in Market.objects.all():
        update_market(market, exchange)
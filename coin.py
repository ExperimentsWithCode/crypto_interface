class Coin():
    def __init__(self, config):
        keys = config.keys()
        self.idx = config["id"] if 'id' in keys else None
        self.name = config["name"] if 'name' in keys else None
        self.symbol = config["symbol"] if 'symbol' in keys else None
        self.rank = config["rank"] if 'rank' in keys else None
        self.price_usd = config["price_usd"] if 'price_usd' in keys else None
        self.price_btc = config["price_btc"] if 'price_btc' in keys else None
        self.daily_volume_usd = config["daily_volume_usd"] if 'daily_volume_usd' in keys else None
        self.market_cap_usd = config["market_cap_usd"] if 'market_cap_usd' in keys else None
        self.available_supply = config["available_supply"] if 'available_supply' in keys else None
        self.total_supply = config["total_supply"] if 'total_supply' in keys else None
        self.max_supply = config["max_supply"] if 'max_supply' in keys else None
        self.percent_change_1h = config["percent_change_1h"] if 'percent_change_1h' in keys else None
        self.percent_change_24h = config["percent_change_24h"] if 'percent_change_24h' in keys else None
        self.percent_change_7d = config["percent_change_7d"] if 'percent_change_7d' in keys else None
        self.last_updated = config["last_updated"] if 'last_updated' in keys else None

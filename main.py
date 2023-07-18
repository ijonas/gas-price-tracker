from time import sleep, time
import requests
import redis
import os
from dotenv import load_dotenv

load_dotenv()
redis_url = os.environ.get('REDIS_URL')
etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')

sources = [
    {"id": "ethereum", "api": f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={etherscan_api_key}", "type": "etherscan"}
]


def initialize_timeseries(ts):
    try:
        retention_msecs = 1000 * 86400 * 365  # 1 year in milliseconds
        ts.create("ethereum-safe", retention_msecs=retention_msecs)
        ts.create("ethereum-propose", retention_msecs=retention_msecs)
        ts.create("ethereum-fast", retention_msecs=retention_msecs)
    except:
        pass


if redis_url is None:
    redis_url = "redis://localhost:6379"
print("Connecting to redis at " + redis_url)
r = redis.Redis.from_url(redis_url, decode_responses=True)
ts = r.ts()
initialize_timeseries(ts)


def main():
    print("Build something amazing today!")

    while True:
        for source in sources:
            try:
                response = requests.get(source["api"])
                data = response.json()
                if data != None and data["status"] == "1":
                    now = int(time() * 1000)
                    ts.add("ethereum-safe", now,
                           float(data["result"]['SafeGasPrice']))
                    ts.add("ethereum-propose", now,
                           float(data["result"]['ProposeGasPrice']))
                    ts.add("ethereum-fast", now,
                           float(data["result"]['FastGasPrice']))
                    print("Added data to redis")
                else:
                    print("Error fetching data from etherscan")
                    print(data)
            except Exception as e:
                print("Error fetching data from etherscan")
                print(e)
        print("Sleeping for 60 seconds")
        sleep(60)


if __name__ == '__main__':
    main()

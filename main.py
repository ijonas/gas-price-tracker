from time import sleep, time
import requests
import redis

sources = [
    {"id": "ethereum", "api": "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=GJ6NWT8ZQCPCKKD3C7W28Q7SKDCTK4ZN3Y", "type": "etherscan"}
]

def initialize_timeseries(ts):
    try:
      retention_msecs = 1000 * 86400 * 365 # 1 year in milliseconds
      ts.create("ethereum-safe", retention_msecs=retention_msecs)
      ts.create("ethereum-propose", retention_msecs=retention_msecs)
      ts.create("ethereum-fast", retention_msecs=retention_msecs)
    except:
       pass

import os
redis_url = os.environ.get('REDIS_URL')
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
          response = requests.get(source["api"])
          data = response.json()
          if data!=None and data["status"] == "1":
            now = int(time() * 1000)
            ts.add("ethereum-safe", now, float(data["result"]['SafeGasPrice']))
            ts.add("ethereum-propose", now, float(data["result"]['ProposeGasPrice']))
            ts.add("ethereum-fast", now, float(data["result"]['FastGasPrice']))
            print("Added data to redis")
          else:
            print("Error fetching data from etherscan")
            print(data)
      print("Sleeping for 60 seconds")
      sleep(60)

if __name__ == '__main__':
    main()
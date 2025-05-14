# A library to add the ability to swap(rotate) proxies easily

This library will provide a Proxy class to manage all of your porxies plus Rotator class to obtain a Proxy based on weights of proxies. An exelent fit for **requests** and **selenium** libraries

## An example usage for "*selenium*" library
``` python
    from proxy_rotator import Proxy, Rotator
    
    proxies: list[Proxy] = []
    # Load proxies from a file
    proxies_json = load_proxies("proxies.json")
    for proxy_item in proxies_json:
        proxies.append(Proxy(
            proxy_item['path'], 
            proxy_item['type'], 
            proxy_item['protocol'],
            proxy_item['status'], 
            proxy_item['weight'])
        )

    # Make a rotation for a proxy
    rotator = Rotator(proxies)
    # Get the random proxy by weight
    proxy = rotator.get()
    # Create a webdriver and put new proxy in use
    firefox_opt = Options()
    firefox_opt.add_argument('--headless')
    firefox_opt.add_argument("--no-sandbox")
    firefox_opt.add_argument("--disable-dev-shm-usage")  
    firefox_opt.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Firefox(options=firefox_opt)
```

## An example usage for "*requests*" library
``` python
    from simple_proxy_rotator import proxy_to_requests_proxy
    from simple_proxy_rotator.proxy_rotator import Proxy, Rotator

    proxies: list[Proxy] = []
    # Load proxies from a file
    proxies_json = load_proxies("proxies.json")
    for proxy_item in proxies_json:
        proxies.append(Proxy(
            proxy_item['path'], 
            proxy_item['type'], 
            proxy_item['protocol'],
            proxy_item['status'], 
            proxy_item['weight'])
        )

    # Make a rotation for a proxy
    rotator = Rotator(proxies)
    # Get the random proxy by weight
    rotator_proxy = rotator_.get()
    # The returned proxy must be convert into string 
    # to be passed to requests.get method
    proxy = proxy_to_requests_proxy(rotator_proxy.ip, rotator_proxy.protocol)
    board_page = requests.get(url=url_, headers=conf.headers, proxies=proxy)
```

## An example of "*proxies.json*" file content
``` json
  {
    "path": "100.100.100.100:1080",
    "protocol": "socks4",
    "type": "mobile",
    "weight": 1250.8024368286133,
    "status": "alive"
  },
  {
    "path": "100.100.100.100:1080",
    "protocol": "http",
    "type": "mobile",
    "weight": 1258.7508733272552,
    "status": "dead"
  },
  {
    "path": "100.100.100.100:1080",
    "protocol": "https",
    "type": "datacenter",
    "weight": 1350.0,
    "status": "alive"
  },
  {
    "path": "100.100.100.100:1080",
    "protocol": "https",
    "type": "datacenter",
    "weight": 850.4147324562073,
    "status": "dead"
  },
  {
    "path": "100.100.100.100:1080",
    "protocol": "socks4",
    "type": "datacenter",
    "weight": 1253.0103130340576,
    "status": "alive"
  },
  {
    "path": "100.100.100.100:1080",
    "protocol": "socks5",
    "type": "datacenter",
    "weight": 1250.8180613517761,
    "status": "alive"
  }
]
```
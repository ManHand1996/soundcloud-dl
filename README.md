# soundcloud-dl
soundcloud music downloader
python: 3.10.8
packages:
```shell
seleniumwire
aiohttp
tqdm
```
required [chromewebdriver](https://sites.google.com/chromium.org/driver/)

edited your proxy:
```python
# webdriver proxy
OPTIONS = {
        'proxy': {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
 }
 # download proxy
 PROXY = 'http://127.0.0.1:7890'
```

```shell
alias soundclound-dl="python3.10 soundcloud_music.py"

```
example:
```shell
soundclound-dl -o ~/Music/CloudMusic https://soundcloud.com/user-502982272/fukin-mixtape
webdriver processing...
Fu©Kin_Mixtape
https://cf-hls-media.sndcdn.com/playlist/h3goFQqrWgrd.128.mp3/playlist.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKjovL2NmLWhscy1tZWRpYS5zbmRjZG4uY29tL3BsYXlsaXN0L2gzZ29GUXFyV2dyZC4xMjgubXAzL3BsYXlsaXN0Lm0zdTgqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjY5MDMwNjk4fX19XX0_&Signature=Xtc7khdif4BzPujjV1LZntIcdRF4of2yf62QksWEDOtUycEP7kK1fw4NEEzo-nnP-MgEMIHHWlx1pXsucW05Haf0VCu8nZqPbqb3Pt1R94hiPsfzmZZURie0aEu56XU9lPqKNLp5klZB4fbmyKYyKL2XLpBAKqwW4X6ScBdbR0dAvIpWazEaQ6UyuaxF6Q9n~d4LkaRy5Sz8kxUSsL0wz9BDoJ~pnA-DiyhDayG3uZWFcolIkH~W~tL7u1aRo-AAlSZ46LqrgF-Z4Rr29iPqp7Wkxlr1euRgZZx1hTFe1PEVv~ndcWbNuBT9rdwBI4MWPu4doWggamdZilrvY44uxQ__&Key-Pair-Id=APKAI6TU7MMXM5DG6EPQ&track_authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJnZW8iOiJISyIsInN1YiI6IiIsInJpZCI6IiIsImlhdCI6MTY2OTAyOTM5Nn0.Ph5T8GbY0FeBM86O8r53wZ1cRPq-jnYA08jbZNYOVrw
#### downloading...
100%|█████████████████████████████████| 120/120 [00:03<00:00, 30.48it/s]
spend 15.363985911000782 second

```




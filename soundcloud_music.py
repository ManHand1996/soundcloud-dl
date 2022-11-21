import os
import sys
from tqdm import asyncio as tqdm_aio
import time
import asyncio
from functools import reduce
from urllib import parse

import aiohttp
import argparse
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BYTES_DICT = {}

OPTIONS = {
        'proxy': {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
 }

TASK_COUNT = 0
FINISH_COUNT = 0

PROXY = 'http://127.0.0.1:7890'


def parse_playlist(data: bytes):
    """return m3u8 list url
    
    Args:
        data (bytes): from webdriver parse data
    
    Returns:
        list of m3u8 url
    """
    m3u8_str = data.decode()
    return list(filter(lambda x: not x.startswith('#'),m3u8_str.splitlines()))
    

def get_url_name(url):
    """the name is BYTES_DICT key, for the dict sorted need m3u8 url sign a name like:
    url = https://cf-hls-media.sndcdn.com/media/159660/0/31762/mm3biiB5eORI.128.mp3
    name = 0+31762 = 31762
    """
    path = parse.urlsplit(url).path
    return reduce(lambda x,y: int(x)+int(y), path.split('/')[3:5])


async def parse_music(url):
    """async get music url content store in BYTES_DICT"""
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=PROXY) as rep:
            name = get_url_name(url)
            
            if rep.status == 200:
                r_content = await rep.content.read()
                BYTES_DICT[name] = r_content
                # print(f'got content with {name}')
            else:
                print(rep.status)
    await asyncio.sleep(1)

async def run_task(url_list: list):
    """create async tasks"""
    tasks = [parse_music(url) for url in url_list]
    TASK_COUNT = len(tasks)
    # process_bar = tqdm_aio.tqdm(total=TASK_COUNT)
    # for f in asyncio.as_completed(tasks):
    #     value = await f
    #     process_bar.set_description(value)
    #     process_bar.update()
    # asyncio.as
    await tqdm_aio.tqdm.gather(*tasks)


def save_music(title: str, save_path=''):
    """save to file"""
    import re
    title = re.sub(r'\W', '', title)
    if save_path:
        save_path = os.path.join(save_path, title+'.mp3')
    else:
        save_path = title + '.mp3'
    
    if BYTES_DICT:
        
        sorted_content = dict(sorted(BYTES_DICT.items(), key=lambda x: x[0]))
        bytes_content = b''.join(sorted_content.values())
        with open(save_path, 'wb') as fb:
            fb.write(bytes_content)
    


def on_webdriver(url: str, save_path: str):
    print('webdriver processing...')
    m3u8_list = []
    
    chrome_option = webdriver.ChromeOptions()
    # firefox_option = webdriver.FirefoxOptions()
    # firefox_option.add_experimental_option("detach", True)
    chrome_option.add_experimental_option("detach", True)  # keep open browser
    # chrome_option.add_argument('--headless')
    # chrome_option.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(chrome_options=chrome_option,seleniumwire_options=OPTIONS)
    # driver = webdriver.Firefox( options=firefox_option,seleniumwire_options=OPTIONS)
    driver.get(url)
    
    driver.implicitly_wait(3)
    delay = 10  # seconds

    try:
        cookie_accept = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                        (By.ID, "onetrust-accept-btn-handler")
                ))
        if cookie_accept:
            cookie_accept.click()
        else:
            print('no accept button')

        title_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH,"//div[@class='soundTitle__titleHeroContainer']/h1/span")
                ))
        
        # driver.find_element(By.XPATH, "//div[@class='soundTitle__titleHeroContainer']/h1/span")
        music_title = title_element.text.replace(' ','_')
        print(music_title)
    except TimeoutException:
        print('Timeout Connect.. please retry')
        quit()
    
    try:
        # using selenium-wire must waitting all related requests of response
        
        r = driver.wait_for_request('/playlist.m3u8', 10)  # waitting specs url but just url string
        print(r.url)
        
        playlist_req = list(filter(lambda x: x.url.find('playlist.m3u8') > 0, driver.iter_requests()))[0]
    except IndexError:
        print('Not found playlist url..')
    else:
        if playlist_req.response:
            # decode and get useful play url
            playlist_req
            m3u8_url_bytes = playlist_req.response.body
            body = decode(m3u8_url_bytes, playlist_req.response.headers.get('Content-Encoding', 'identity'))
            
            m3u8_list = parse_playlist(body)
    finally:
        driver.quit()

    if m3u8_list:
        print('#### downloading...')
        asyncio.run(run_task(m3u8_list))
        save_music(music_title, save_path)


def main():
    """命令行参数
    In Terminal run:
    python soundclound_music.py [-o] url
    option args:
        -o --output: download path of music
    """
    
    arg_parser = argparse.ArgumentParser(description="soundcloud downloader")
    arg_parser.add_argument('-o', '--output', type=str, required=False, help='download path of music',)
    arg_parser.add_argument('url', type=str)
    args = arg_parser.parse_args()
    
    url = args.url
    save_path = args.output
    
    # url = 'https://soundcloud.com/user-502982272/fukin-mixtape'
    # save_path = '~/Music/CloudMusic'
    
    parse_result = parse.urlparse(url)
    if not parse_result.scheme or not parse_result.netloc:
        print('please input a valid url')
        quit()
    
    start_perf = time.perf_counter()
    on_webdriver(url, save_path)
    end_perf = time.perf_counter()
    print(f'spend {end_perf - start_perf} second')

if __name__ == '__main__':
    
   
    # url = 'https://soundcloud.com/user-502982272/cop-tale-1'
    
    main()

    # for i in range(10):
    #     print("\r",'#' * i, end='', flush=True)
    #     time.sleep(1)
    
    # print('\nfinish')
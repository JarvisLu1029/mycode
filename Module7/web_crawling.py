from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import queue
import time

# 創建一個 Options 物件
chrome_options = Options()

chrome_options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗
chrome_options.add_argument("--incognito") # 無痕模式
chrome_options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(ChromeDriverManager("120.0.6099.109").install(), options=chrome_options)

# Momo
def momo_data(queue, commodity):
    driver.get(f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={commodity}')

    commodity_names = driver.find_elements(By.XPATH, "//div[@class='prdNameTitle']/h3[@class='prdName']")
    commodity_images = driver.find_elements(By.XPATH, "//Img[@class='prdImg' and contains(@src, 'goodsimg')]")
    value_elements = driver.find_elements(By.XPATH, "//p[@class='money']/span[@class='price']/b")
    commodity_links = driver.find_elements(By.XPATH, "//a[@class='goodsUrl' and contains(@href, 'goods')]")

    info_dict = {}
    for i in range(len(commodity_names)):
        info_dict[f'{i}'] = {
            'commodity_name': commodity_names[i].text,
            'commodity_image': commodity_images[i].get_attribute('src'),
            'commodity_value': value_elements[i].text,
            'commodity_link': commodity_links[i].get_attribute('href'),
            'store': 'MOMO'
            }
        
    queue.put(info_dict)

    return info_dict

def carrefour_data(queue, commodity):
    driver.get(f'https://online.carrefour.com.tw/zh/search/?q={commodity}')
    
    commodity_names = driver.find_elements(By.XPATH, "//div[@class='commodity-desc']/div/a")
    commodity_images = driver.find_elements(By.XPATH, "//img[@class='m_lazyload']")
    value_elements = driver.find_elements(By.XPATH, "//div[@class='current-price']")
    commodity_links = driver.find_elements(By.XPATH, "//a[@class='gtm-product-alink']")

    info_dict = {}
    for i in range(len(commodity_names)):
        info_dict[f'{i}'] = {
            'commodity_name': commodity_names[i].text,
            'commodity_image': commodity_images[i].get_attribute('src'),
            'commodity_value': value_elements[i].text,
            'commodity_link': commodity_links[i].get_attribute('href'),
            }
    
    queue.put(info_dict)

    return info_dict

def pchome_data(queue, commodity):
    driver.get(f'https://ecshweb.pchome.com.tw/search/v3.3/?q={commodity}')

    scroll_height(driver)
                                                # 找到所有 <h5 class='prod_name> 底下的 <a> '
    commodity_names = driver.find_elements(By.XPATH, "//h5[@class='prod_name']/a")
    commodity_images = driver.find_elements(By.XPATH, "//a[@class='prod_img']/img")
    value_elements = driver.find_elements(By.XPATH, "//ul[@class='price_box']/li/span/span[@class='value']")

    info_dict = {}
    for i in range(len(commodity_names)):
        info_dict[f'{i}'] = {
            'commodity_name': commodity_names[i].text,
            'commodity_image': commodity_images[i].get_attribute('src'),
            'commodity_value': value_elements[i].text,
            'commodity_link': commodity_names[i].get_attribute('href'),
            'store': 'PChome'
            }
        
    queue.put(info_dict)

    return info_dict

def pxmart_data(queue, commodity):
    driver.get(f'https://www.pxmart.com.tw/#/search-result/{commodity}')
    
    commodity_names = driver.find_elements(By.XPATH, "//p[@class='line-clamp-3']")
    commodity_images = driver.find_elements(By.XPATH, "//div[@class='productImg']/img")
    value_elements = driver.find_elements(By.XPATH, "//span[@class='price']")
    commodity_links = driver.find_elements(By.XPATH, "//div[@class='activity-product-fix']/a")

    info_dict = {}
    for i in range(len(commodity_names)):
        info_dict[f'{i}'] = {
            'commodity_name': commodity_names[i].text,
            'commodity_image': commodity_images[i].get_attribute('src'),
            'commodity_value': value_elements[i].text,
            'commodity_link': commodity_links[i].get_attribute('href'),
            }
    
    queue.put(info_dict)

    return info_dict


def scroll_height(driver):
    '''
    innerHeight => 瀏覽器內部的高度
    offset => 當前捲動的量(高度)
    count => 累計無效滾動次數
    limit => 最大無效滾動次數
    '''
    innerHeight = 0
    offset = 0
    count = 0
    limit = 3
    # 在捲動到沒有元素動態產生前，持續捲動
    while count <= limit:
        # 每次移動高度
        offset = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        )
        # 捲軸往下滑動
        driver.execute_script(f'''
            window.scrollTo({{
                top: {offset}, 
                behavior: 'smooth' 
            }});
        ''')
        
        # 強制等待，此時若有新元素生成，瀏覽器內部高度會自動增加
        time.sleep(3)

        # 透過執行 js 語法來取得捲動後的當前總高度
        innerHeight = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        )

        # 經過計算，如果滾動距離(offset)大於等於視窗內部總高度(innerHeight)，代表已經到底了
        if offset == innerHeight:
            count += 1
                
        # 為了實驗功能，捲動超過一定的距離，就結束程式
        if offset >= 1800:
            break
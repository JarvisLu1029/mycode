from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, os

image_list = []

def get_twitter_image():
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

    my_options = webdriver.ChromeOptions()
    my_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    
    token = "token" 
    # 創建 cookie 對象
    cookie = {
    "name": "auth_token",  # 替換成您要設置的 cookie 名稱
    "value": token,  # 替換成您要設置的 token 值
    "domain": "twitter.com",  # 替換成您要設置的網域
    "Path": "/"
    }

    my_service = Service(executable_path="E:\Program\web_scraping\practice\chromedriver.exe")
    driver = webdriver.Chrome(
        options = my_options,
        service=my_service
    )
    
    driver.get('https://twitter.com/_ai_mayu_')
    # 添加 cookie
    driver.add_cookie(cookie)
    # 刷新網頁
    driver.refresh()

    if not os.path.exists('data.txt'):
        # 如果檔案不存在，則創建新檔案
        with open('data.txt', 'w'):
            pass
    # 讀取檔案
    with open('data.txt', 'r') as f:
        existing_data = f.readlines()
        # 移除每一行的換行符
        existing_data = [line.strip() for line in existing_data]
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

        image_elements = driver.find_elements(By.CLASS_NAME, "css-9pa8cd")  # 替换成您要抓取的图片元素的类名

        for i in image_elements:
            image_url = i.get_attribute('src')
            if 'medium' in image_url and image_url not in image_list:
                image_list.append(image_url)
                if image_url not in existing_data:
                    # 寫入資料
                    with open('data.txt', 'a') as f:
                        f.write(image_url + "\n")
                else:
                    print("Data already exists in the file.")

        # 透過執行 js 語法來取得捲動後的當前總高度
        innerHeight = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        )
        
        # 經過計算，如果滾動距離(offset)大於等於視窗內部總高度(innerHeight)，代表已經到底了
        if offset == innerHeight:
            count += 1
				
				# 為了實驗功能，捲動超過一定的距離，就結束程式
        if offset >= 36000:
            print(image_list)
            break

if __name__=="__main__":
    get_twitter_image()

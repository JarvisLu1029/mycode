import requests
from bs4 import BeautifulSoup as bs
import re


def search_yahoo_movie(movie_name):
    url = "https://movies.yahoo.com.tw/moviesearch_result.html"

    params = {'movie_type': 'all', 'keyword': f'{movie_name}'}

    response = requests.get(url, params=params)
    soup = bs(response.text, "lxml")
    movie_info = soup.select_one('div.release_movie_name a')['href']

    return movie_info

def get_comment_link():
    url = search_yahoo_movie(movie_name)
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    # <a href="https://movies.yahoo.com.tw/movieinfo_review.html/id=14653" 
    # class="gabtn" data-ga="['電影頁tab','電影頁tab_網友短評','']">網友短評</a>
    link = soup.select_one('a[data-ga*="網友短評"]')['href']
    
    return link

def get_comments(url):
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    get_movie_name = soup.select_one('h1.inform_title').get_text(strip=True).split()[0]
    satisfaction = soup.select_one('span[data-num]')['data-num']
    user_comment_list = soup.select('ul.usercom_list li')

    re_dict = {}
    re_dict['search_result'] = get_movie_name
    re_dict['綜合評分:'] = satisfaction
    regex_comment = r'<span>(.*?)</span>'
    regex_score = r'score.+value="(\d)"'
    com_cnt = 1
    for i in user_comment_list:
        user_comment = re.findall(regex_comment, f'{i}', re.DOTALL)[0]
        score = re.findall(regex_score, f'{i}')[0]
        dict2 = {f'{com_cnt}. {(int(score)*"★ ")}': f'{user_comment}'}
        re_dict.update(dict2)
        com_cnt +=1
    return re_dict

def get_movie_post():
    url = search_yahoo_movie(movie_name)
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    post_url = soup.select_one('div.movie_intro_foto img')['src']

    return post_url
def get_comment_next_page():
    url = get_comment_link()
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    next_page = soup.select_one('a[rel="next"]')['href']

    return f'https://movies.yahoo.com.tw/{next_page}'




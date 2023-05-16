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
    info_dict = {}
    url = search_yahoo_movie(movie_name)
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    # <a href="https://movies.yahoo.com.tw/movieinfo_review.html/id=14653" 
    # class="gabtn" data-ga="['電影頁tab','電影頁tab_網友短評','']">網友短評</a>
    link = soup.select_one('a[data-ga*="網友短評"]')['href']
    post_url = soup.select_one('div.movie_intro_foto img')['src']
    get_movie_name = soup.select_one('div.movie_intro_info_r h1').get_text()
    movie_name_en = soup.select_one('div.movie_intro_info_r h3').get_text()
    info_dict.update({
        'link':link, 'post_url':post_url, 'movie_name':get_movie_name, 'movie_name_en':movie_name_en
    })

    return info_dict

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

def get_comment_next_page():
    url = get_comment_link()
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    next_page = soup.select_one('a[rel="next"]')['href']

    return f'https://movies.yahoo.com.tw/{next_page}'

# 台北票房榜的電影資訊
def get_movie_ranks():
    url = "https://movies.yahoo.com.tw/"
    response = requests.get(url)
    soup = bs(response.text, "lxml")
    movie_ranks = soup.select('ul.ranking_list_r a')
    movie_rank_urls = re.findall(r'href=\"(.+)\"' , f'{movie_ranks}')

    movie_info_dict = {}
    for movie_rank_url in movie_rank_urls:
        movie_rank = requests.get(movie_rank_url)
        movie_soup = bs(movie_rank.text, "lxml")
        get_movie_name = movie_soup.select_one('div.movie_intro_info_r h1').get_text()
        movie_image = movie_soup.select_one('div.movie_intro_foto img')['src']
        movie_score = movie_soup.select_one('div.score_num').get_text()
        movie_comment_url = movie_soup.select_one('a[data-ga*="網友短評"]')['href']
        movie_info_dict.update({
            get_movie_name: {"img": movie_image, "score": movie_score, "comment_url": movie_comment_url}
            })
        
    return movie_info_dict
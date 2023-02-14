import csv
import datetime
import requests
from bs4 import BeautifulSoup

def create_soup(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.18.154.7 Safari/537.36'}
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'lxml')

    return soup

def extract_movie_daum(start=datetime.date.today().year - 11, end=datetime.date.today().year - 1):
    if start < 2004 or end > datetime.date.today().year - 1:
        print('[ERROR] 영화 정보가 없습니다. 올바른 연도를 입력하세요.')
        return 
    
    result = []
    
    for year in range(start, end + 1):
        
        soup = create_soup(f'https://movie.daum.net/ranking/boxoffice/yearly?date={year}')
        
        movie_list = soup.find('ol', attrs={'class':'list_movieranking'})
        
        movies = movie_list.find_all('li')
        
        for movie in movies:
            title = movie.find('a', attrs={'class':'link_txt'}).get_text()
            link = 'https://movie.daum.net' + movie.find('a', attrs={'class':'link_txt'})['href']
            release = movie.find('span', attrs={'class':'txt_num'}).get_text()
            audience = movie.find_all('span', attrs={'class':'info_txt'})[1].get_text().replace('관객수', '').replace('명', '')
            rank = movie.find('span', attrs={'class':'rank_num'}).get_text()
            tag = movie.find('span', attrs={'class':'txt_tag'}).get_text().strip()
            summary = movie.find('a', attrs={'class':'link_story'}).get_text().strip().replace('\r', '').replace('\n', '')
            
            movie_data = {
                'year': year,
                'rank': rank,
                'title': title,
                'release': release,
                'audience': audience,
                'tag': tag,
                'summary': summary,
                'link': link,
            }
            
            if link == 'https://movie.daum.net/moviedb/main?movieId=':
                continue
            
            result.append(movie_data)

    return result

def save_to_file(filename, movies):
    file = f'{filename}.csv'
    f = open(file, 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)

    title = ['연도', '순위', '제목', '개봉일', '관객수', '관람등급', '줄거리', '링크']
    writer.writerow(title)

    for movie in movies:
        writer.writerow(list(movie.values()))

    f.close()
    
def main():
    movies = extract_movie_daum()
    save_to_file('movies', movies)
    
if __name__ == '__main__':
    main()
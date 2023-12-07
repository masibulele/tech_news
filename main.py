from flask import Flask, render_template
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os, json

load_dotenv()
api_key = os.getenv('api_key')

app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def home():
    latest_articles= get_news_headlines()
    clean_articles = [item for item in latest_articles if item['article_snip']!='None']
    return render_template('index.html',all_data=clean_articles,count=0)


def get_news_headlines():
    load_dotenv()
    news_api = NewsApiClient(api_key=api_key)
    headlines_tech= news_api.get_top_headlines(country='us', category='technology', )
    headlines_business= news_api.get_top_headlines(category='business')
    articles_list = []
    articles = headlines_tech['articles']+headlines_business['articles']
    
    for article in articles:
        if (article['urlToImage'] !=None or article['content'] !=None):
            new_dict={
                'title': article['title'],
                'image_url': article['urlToImage'],
                'article_snip': str(article['content']).split('[')[0],
                'url': article['url']

            }
            articles_list.append(new_dict)
        else:
            pass
        
         
    return  articles_list



if __name__== "__main__":
    # test=get_news_headlines()
    # clean=[item for item in test if item['article_snip']!='None']
    # print(clean)
    app.run(debug=True)
    
import requests

import json

from joblib import Parallel, delayed

from get_qiita_items import *

BASE_API_URL = 'https://qiita.com/api/v2/'


def get_comments_items(qiita_api_token, check_date):
  """Qiita APIを利用して記事一覧を取得する
  Args:
        qiita_api_token (string): Qiitaのアプリケーショントークン
  """
  headers = {'Authorization': f'Bearer {qiita_api_token}'}
  query = f'created:>={check_date}'
  items = get_items(qiita_api_token, query)

  return items

def get_comments_count_ranking(qiita_api_token, check_date, comments_count):
  """記事一覧を取得してストック数ランキングを生成する
  """
  allItems = get_comments_items(qiita_api_token, check_date)
  rankingList = list(filter(lambda x: x['comments_count'] >= comments_count, format_items(allItems)))
  rankingList.sort(key=lambda x: (x['comments_count'], x['likes_count']), reverse=True)
  return rankingList

import requests

import json

from joblib import Parallel, delayed

from get_qiita_items import *

BASE_API_URL = 'https://qiita.com/api/v2/'


def get_stokers_items(qiita_api_token, check_date, stockers_clount=10):
  """Qiita APIを利用して記事一覧を取得する
  Args:
        qiita_api_token (string): Qiitaのアプリケーショントークン
  """
  headers = {'Authorization': f'Bearer {qiita_api_token}'}
  query = f'created:>={check_date} stocks:>={stockers_clount}'
  items = get_items(qiita_api_token, query)

  # for item in items:
  #   get_item_detail(headers, item)
  items = Parallel(n_jobs=-1, verbose=0)(
    [delayed(get_item_detail)(headers, item) for item in items])
  return items

def get_stokers_count_ranking(qiita_api_token, check_date, stockers_clount=10):
  """記事一覧を取得してストック数ランキングを生成する
  """
  allItems = get_stokers_items(qiita_api_token, check_date, stockers_clount)
  rankingList = format_items(allItems)
  rankingList.sort(key=lambda x: (x['stockers_count'], x['likes_count']), reverse=True)
  return rankingList

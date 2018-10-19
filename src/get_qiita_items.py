import requests

import json

from joblib import Parallel, delayed


BASE_API_URL = 'https://qiita.com/api/v2/'


def get_items(qiita_api_token, query):
  """Qiita APIを利用して記事一覧を取得する
  Args:
        qiita_api_token (string): Qiitaのアプリケーショントークン
  """
  headers = {'Authorization': f'Bearer {qiita_api_token}'}
  params = {
    'page': 1,
    'per_page': 100,
    'query': query
  }

  itemsUrl = f'{BASE_API_URL}items'
  page = 0
  allItems = []
  while True:
    page += 1
    params['page'] = page
    itemsRes = requests.get(itemsUrl, headers=headers, params=params)
    itemsRes.raise_for_status()
    items = json.loads(itemsRes.text)
    if len(items) == 0:
      break
    if len(allItems) == 0:
      allItems = items
    else:
      allItems.extend(items)
  return allItems


def get_item_detail(headers, item):
  """Qiita APIを利用してViewsとストック数を含めて記事を取得する
  Args:
        headers (dict): アクセストークンを含めたリクエストヘッダー情報
        item (dict): Qiitaの記事情報
  """
  itemId = item['id']

  try:
  # 記事IDからストック数を取得する
    stokersUrl = f'{BASE_API_URL}items/{itemId}/stockers'
    stokersRes = requests.get(stokersUrl, headers=headers)
    stokersRes.raise_for_status()
    item['stockers_count'] = int(stokersRes.headers.get('Total-Count'))
  finally:
    # エラーが発生しても無視して返す
    return item

def format_items(allItems):
  """記事一覧から必要な項目のみ抽出する
  """
  formatedItems = []
  for item in allItems:
    stockers_count = 0
    if item and 'stockers_count' in item:
      stockers_count = item['stockers_count']

    formatedItems.append({
      'title': item['title'],
      'url': item['url'],
      'user_id': item['user']['id'],
      'stockers_count': stockers_count,
      'likes_count': item['likes_count'],
      'comments_count': item['comments_count'],
      'tags': item['tags'],
      'created_at': item['created_at']
    })
  return formatedItems
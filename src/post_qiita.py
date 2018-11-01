import datetime

import json

import requests

BASE_API_URL = 'https://qiita.com/api/v2/items/'


def post_stokers_ranking(qiita_api_token, item_id, check_date, stockers_clount, rankingItems):
  body = create_stokers_ranking_body(check_date, stockers_clount, rankingItems)
  putPrms = {
    'title': 'Qiita週間ストック数ランキング【自動更新】',
    'body': body
  }

  response = requests.patch(
    f'{BASE_API_URL}{item_id}',
    json.dumps(putPrms),
    headers={
      'Authorization': f'Bearer {qiita_api_token}',
      'Content-Type': 'application/json',
    })
  print(response)

def create_stokers_ranking_body(check_date, stockers_clount, rankingItems):
  startDate = datetime.datetime.now().strftime('%Y-%m-%d')
  updateDate = datetime.datetime.now().strftime('%Y-%m-%d %H時')
  header = f"""
直近でストック数が多い記事を自動で集計して投稿できるようにしてみました。
いいねが少ないけどストック数が多い良記事がきっと眠っているはず！！！

※不具合などもし気が付かれましたらお知らせいただけると嬉しいです。

#### 集計方法
- 集計方法: 8時間ごとにQiita API v2を利用して集計 (**{updateDate}**更新)
- 集計期間: **{check_date}** から **{startDate}** に投稿された記事
- ストック数: **{stockers_clount}**以上ストックされた記事

"""

  itemBodys = []
  rank = 0
  for item in rankingItems:
    rank += 1
    tags = item['tags']
    tags_str = ""
    for tag in tags:
      tags_str += f'```{tag["name"]} ``` '

    createAt = item['created_at'].replace('+09:00', '+0900')
    createAt = datetime.datetime.strptime(createAt, '%Y-%m-%dT%H:%M:%S%z')
    createAt = createAt.strftime('%Y-%m-%d %H時')
    itemBodys.append(f"""
## {rank}位 [{item['title']}]({item['url']})

**{item['stockers_count']}**ストック　**{item['likes_count']}**いいね / [{item['user_id']}](https://qiita.com/{item['user_id']}) さん {createAt}投稿
{tags_str}

""")

  return header + ''.join(itemBodys)


def post_comments_ranking(qiita_api_token, item_id, check_date, comments_count, rankingItems):
  body = create_comments_ranking_body(check_date, comments_count, rankingItems)
  putPrms = {
    'title': 'Qiita週間コメント数ランキング【自動更新】',
    'private': True,
    'body': body
  }

  response = requests.patch(
    f'{BASE_API_URL}{item_id}',
    json.dumps(putPrms),
    headers={
      'Authorization': f'Bearer {qiita_api_token}',
      'Content-Type': 'application/json',
    })
  print(response)

def create_comments_ranking_body(check_date, comments_count, rankingItems):
  startDate = datetime.datetime.now().strftime('%Y-%m-%d')
  updateDate = datetime.datetime.now().strftime('%Y-%m-%d %H時')
  header = f"""
直近でコメントがついて盛り上がってる？記事を自動で集計して投稿できるようにしてみました。
コメントされるってことは良い記事か、良い議論がされてるに違いない！

※不具合などもし気が付かれましたらお知らせいただけると嬉しいです。

#### 集計方法
- 集計方法: 8時間ごとにQiita API v2を利用して集計 (**{updateDate}**更新)
- 集計期間: **{check_date}** から **{startDate}** に投稿された記事
- コメント数: **{comments_count}**以上コメントされた記事

"""

  itemBodys = []
  rank = 0
  for item in rankingItems:
    rank += 1
    tags = item['tags']
    tags_str = ""
    for tag in tags:
      tags_str += f'```{tag["name"]} ``` '

    createAt = item['created_at'].replace('+09:00', '+0900')
    createAt = datetime.datetime.strptime(createAt, '%Y-%m-%dT%H:%M:%S%z')
    createAt = createAt.strftime('%Y-%m-%d %H時')
    itemBodys.append(f"""
## {rank}位 [{item['title']}]({item['url']})

**{item['comments_count']}**コメント　**{item['likes_count']}**いいね / [{item['user_id']}](https://qiita.com/{item['user_id']}) さん {createAt}投稿
{tags_str}

""")

  return header + ''.join(itemBodys)

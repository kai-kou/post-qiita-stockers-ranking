import datetime

import os

from src.get_qiita_stokers import *

from src.post_qiita import *


def post_stokers_ranking_handler(event, context):
  qiita_api_token = os.environ['QIITA_API_TOKEN']
  stockers_count = os.environ['STOCKERS_COUNT']
  item_id = os.environ['QIITA_ITEM_ID']

  startDate = datetime.datetime.now()
  startDate = (startDate - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")

  rankingList = get_stokers_count_ranking(qiita_api_token, startDate, stockers_count)
  post_stokers_ranking(qiita_api_token, item_id, startDate, stockers_count, rankingList)

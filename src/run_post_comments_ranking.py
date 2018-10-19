import datetime

from get_qiita_comments_items import *

from post_qiita import *

from docopt import docopt

import json

# use CLI
if __name__ == '__main__':
  _USAGE = '''
  Qiita APIからコメント数ランキングを生成してQiitaへ投稿する
  Usage:
    run_post_stokers_ranking.py <qiita_api_token> <item_id>
    run_post_stokers_ranking.py --help
  '''

  options = docopt(_USAGE)

  qiita_api_token = options['<qiita_api_token>']
  item_id = options['<item_id>']
  startDate = datetime.datetime.now()
  startDate = (startDate - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
  comments_count = 5

  rankingList = get_comments_count_ranking(qiita_api_token, startDate, comments_count)

  post_comments_ranking(qiita_api_token, item_id, startDate, comments_count, rankingList)

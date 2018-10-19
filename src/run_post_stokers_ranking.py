import datetime

from get_qiita_stokers import *

from post_qiita import *

from docopt import docopt


# use CLI
if __name__ == '__main__':
  _USAGE = '''
  Qiita APIからストック数ランキングを生成してQiitaへ投稿する
  Usage:
    get_qiita_items.py <qiita_api_token> <item_id>
    get_qiita_items.py --help
  '''

  options = docopt(_USAGE)

  qiita_api_token = options['<qiita_api_token>']
  item_id = options['<item_id>']
  startDate = datetime.datetime.now()
  startDate = (startDate - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
  stockers_count = 10

  rankingList = get_stokers_count_ranking(qiita_api_token, startDate, stockers_count)

  post_stokers_ranking(qiita_api_token, item_id, startDate, stockers_count, rankingList)

# post-qiita-stockers-ranking

Qiita週間ストック数ランキングを集計してQiitaに投稿する  


## Install

```sh
> git clone https://github.com/kai-kou/post-qiita-stockers-ranking.git
> cd post-qiita-stockers-ranking
> python -b venv venv
> . venv/bin/activate
> cd src
> pip install -r requirements.txt
```

## Usage

※投稿するQiita記事は事前にQiitaサイトで投稿しておく前提  

```sh
> cd post-qiita-stockers-ranking
> python src/run_post_stokers_ranking.py <Qiitaのアクセストークン> <投稿するQiita記事のID>
```

## Deploy

### AWS Lambda

※投稿するQiita記事は事前にQiitaサイトで投稿しておく前提  

```sh
> aws configure

> aws iam create-role --role-name post_qiita_stokers_ranking_exec_role \
  --assume-role-policy-document settings/role-policy.json

> aws iam get-role --role-name post_qiita_stokers_ranking_exec_role

> aws iam get-policy --policy-arn "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"

> aws iam attach-role-policy --role-name post_qiita_stokers_ranking_exec_role \
  --policy-arn "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"

> aws iam list-attached-role-policies --role-name post_qiita_stokers_ranking_exec_role

> cd post-qiita-stockers-ranking/src

> pip install -r requirements.txt -t deploy

> cp *.py deploy

> cd deploy

> zip -r lambda.zip *

> aws lambda create-function \
  --function-name post_qiita_stokers_ranking \
  --region ap-northeast-1 \
  --zip-file fileb://lambda.zip \
  --role arn:aws:iam::xxxxxxxxxxxx:role/post_qiita_stokers_ranking_exec_role \
  --handler lambda.post_stokers_ranking_handler \
  --runtime python3.6 \
  --timeout 300 \
  --memory-size 1024

# 環境変数の設定はAWSマネジメントコンソールで行ってください
#  - QIITA_API_TOKEN: Qiitaのアクセストークン
#  - STOCKERS_COUNT: 集計対象とするストック数
#  - QIITA_ITEM_ID: 投稿するQiita記事のID

# トリガー設定はAWSマネジメントコンソールで行ってください
```

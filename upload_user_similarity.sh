python recs/core/reformat_as_csv.py user:users recs/output/user_similarity.txt recs/output/user_similarity.csv
.google_appengine/appcfg.py upload_data --config_file=bulkloader.yaml --filename=recs/output/user_similarity.csv --kind=Recommendation --url=http://inforlearn.appspot.com/remote_api -e AloneRoad@Gmail.com
mv bulkloader-* bulkloader_logs

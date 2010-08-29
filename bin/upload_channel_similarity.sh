python recs/core/reformat_as_csv.py channel:channels recs/output/channel_similarity.txt recs/output/channel_similarity.csv
.google_appengine/appcfg.py upload_data --config_file=bulkloader.yaml --filename=recs/output/channel_similarity.csv --kind=Recommendation --url=http://inforlearn.appspot.com/remote_api -e AloneRoad@Gmail.com
mv bulkloader-* bulkloader_logs


#from ast import literal_eval
#
#class RecommendationEngine:
#  def __init__(self, data_file="recs_data.txt"):
#    self.lines = open(data_file).read().split("\n")
#    
#  def load_to_memory(self):
#    recs_data = {}
#    for line in self.lines:
#      owner, actors = line.split("  ")
#      owner = literal_eval(owner)
#      actors = literal_eval(actors)
#      recs_data[owner] = actors
#    return recs_data
#
#  def get_recommended(self, actor, recs_data):
#    return recs_data[actor]
#
#
#if __name__ == "__main__":
#  rs = RecommendationEngine()
#  recs_data = rs.load_to_memory()
#  for i in rs.get_recommended("#videostreaming@inforlearn.appspot.com", recs_data):
#    print i

from common.models import Recommendation

params = {"key_name": "user:users/Admin@inforlearn.appspot.com",
        "items": "[(0.40824829046386296, 'AloneRoad@inforlearn.appspot.com')]"
        }
item = Recommendation(**params)
item.put()
#! coding: utf-8
## Recommendation Engine with Map/Reduce and Dumbo
#
# Implement Amazon's style Recommendations
# (Item-to-Item Collaborative Filtering)
# 
# similarity(vector(A), vector(B)) = cosine(vector(A), vector(B))
#
#                                           vector(A) dot vector(B) 
#                                  = -------------------------------------
#                                    length(vector(A)) * length(vector(B))
#
# more info: see Amazon-Recommendations.pdf in this folder

from heapq import nlargest
from math import sqrt
from itertools import chain
from dumbo import main

seperate_character = "\t"

## General functions
#
def sum_reducer(key, values):
    yield key, sum(values)

def n_largest_reducer(n, key=None):
    def reducer(_key, values):
        yield _key, nlargest(n, chain(*values), key=key)
    return reducer

def n_largest_combiner(n, key=None):
    def combiner(_key, values):
        yield _key, nlargest(n, values, key=key)
    return combiner

## Calcule similarity between elements via 5 steps
#
def mapper_1(key, value):
  owner, actor = value.split(seperate_character)
  yield (owner, actor), 1

def mapper_2(key, value):
  yield key[0], (value, key[1])

def reducer_2(key, values):
  values = nlargest(1000, values)
  norm = sqrt(sum(value[0]**2 for value in values))
  for value in values:
    yield (value[0], norm, key), value[1]

def mapper_3(key, value):
  yield value, key

def mapper_4(key, value):
  for _key, _value in ((k, v) for k in value \
                              for v in value \
                              if k != v):
    yield (_key[1:], _value[1:]), _key[0] * _value[0]

def mapper_5(key, value):
  _key, _value = key
  yield _key[1], (value / (_key[0] * _value[0]), _value[1])

## Map/Reduce runner
#
def runner(job):
  job.additer(mapper_1, sum_reducer, combiner=sum_reducer)
  job.additer(mapper_2, reducer_2)
  job.additer(mapper_3, n_largest_reducer(10000), n_largest_combiner(10000))
  job.additer(mapper_4, sum_reducer, combiner=sum_reducer)
  job.additer(mapper_5, n_largest_reducer(100), n_largest_combiner(100))

if __name__ == "__main__":
  main(runner)
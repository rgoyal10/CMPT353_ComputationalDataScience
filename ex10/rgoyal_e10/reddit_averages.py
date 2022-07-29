import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit averages').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)
    #comments.show();
    
    # TODO: calculate averages, sort by subreddit. Sort by average score and output that too.
    
    #sort by subreddit name
    #comments.select('subreddit').show();
    subreddit_groups = comments.groupBy('subreddit').avg('score')
    subreddit_groups = subreddit_groups.withColumnRenamed('avg(score)','score')  #referred to https://sparkbyexamples.com/pyspark/pyspark-rename-dataframe-column/
    
    subreddit_groups = subreddit_groups.cache();
    
    #subreddit_groups.show();
    
    averages_by_subreddit = subreddit_groups.sort('subreddit')
    #averages_by_subreddit.show();
    
    averages_by_score = subreddit_groups.orderBy('score',ascending = False) #referred to https://stackoverflow.com/questions/34514545/spark-dataframe-groupby-and-sort-in-the-descending-order-pyspark
    #averages_by_score.show();
    
    
    
    averages_by_subreddit.write.csv(out_directory + '-subreddit', mode='overwrite')
    averages_by_score.write.csv(out_directory + '-score', mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

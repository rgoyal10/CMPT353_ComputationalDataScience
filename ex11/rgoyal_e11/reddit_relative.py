import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
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
    
    comments = comments.select (comments['subreddit'],comments['score'],comments['author'])
    #comments.show()
    comments = comments.cache()
    
    subreddit_groups = comments.groupBy('subreddit').avg('score')
    subreddit_groups = subreddit_groups.filter(subreddit_groups['avg(score)'] > 0)
    #subreddit_groups.show()
  
    joined_data = comments.join(subreddit_groups.hint('broadcast'), on = 'subreddit')
    joined_data = joined_data.withColumn('rel_score', joined_data['score']/joined_data['avg(score)'])
    joined_data = joined_data.cache()
    #joined_data.show()
    
    max_joined = joined_data.groupBy('subreddit').max('rel_score')
    max_joined = max_joined.withColumnRenamed('max(rel_score)','rel_score')
    #max_joined.show()
    
    joined_data = joined_data.withColumnRenamed('subreddit','subreddit_name')
    best_author = joined_data.join(max_joined.hint('broadcast'), on = 'rel_score')
    #best_author.show()
    
    
    
    best_author = best_author.select( best_author['subreddit'], best_author['author'],best_author['rel_score'])
    #best_author.show()
    
    # TODO

    best_author.write.json(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

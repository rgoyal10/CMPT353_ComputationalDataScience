import sys
from pyspark.sql import SparkSession, functions, types
import re
import string

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+



def main(in_directory, out_directory):
    df = spark.read.text(in_directory)
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
    df = df.withColumn('value',functions.split('value',wordbreak))
    
    df = df.withColumn('value',functions.explode('value'))
    df = df.withColumn('value',functions.lower('value'))
   
    
    df = df.groupBy('value').count()
    
    
    df = df.sort(df['count'].desc(),df['value'].asc())
    
    df = df.filter(df['value'] != '')
    
    
    
    df.write.csv(out_directory, mode = 'overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

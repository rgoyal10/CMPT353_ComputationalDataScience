import sys
from pyspark.sql import SparkSession, functions, types
import re

spark = SparkSession.builder.appName('reddit averages').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wiki_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('requests', types.LongType()),
    types.StructField('bytes', types.LongType()),
   
])

def extract_date(path):
    x = path.split('-')
    return x[2] + '-' + x[3][0] + x[3][1]
	

def main(in_directory, out_directory):
    pagecount = spark.read.csv(in_directory, sep = ' ' , schema = wiki_schema ).withColumn('filename', functions.input_file_name())
    #pagecount.show();
    
    pagecount = pagecount.filter(pagecount.language == 'en')
    pagecount = pagecount.filter(pagecount.title != 'Main_Page')
    pagecount= pagecount.filter(pagecount.title.startswith('Special:') == False) #referred to https://stackoverflow.com/questions/45552293/spark-data-frame-search-column-starting-with-a-string
    
    converted = functions.udf(lambda z: extract_date(z), types.StringType() ) #referred to https://sparkbyexamples.com/pyspark/pyspark-udf-user-defined-function/
    pagecount = pagecount.withColumn('date_hour', converted(pagecount.filename) )
    #pagecount.show();
    
    grouped = pagecount.groupBy('date_hour').max('requests')
    grouped = grouped.withColumnRenamed('max(requests)','requests')
    #grouped.show();
    
    grouped.cache();
    
    final_data = grouped.join(pagecount, ['date_hour','requests'])
    final_data = final_data.sort('date_hour','title')
    final_data = final_data.drop('language','bytes','filename')
    final_data = final_data.select('date_hour','title','requests')
    #final_data.show();
    
    final_data.write.csv(out_directory, mode='overwrite')




if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
import math

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        return Row(hostname = m[1],bytes = m[2])
    else:
    	return None;


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # TODO: return an RDD of Row() objects
    rows = log_lines.map(line_to_row)
    rows = rows.filter(not_none)
    return rows
    


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    # TODO: calculate r.
    grouped_names = logs.groupBy('hostname').count()
    grouped_bytes = logs.groupBy('hostname').agg(functions.sum('bytes'))
    
    #grouped_names.show()
    #grouped_bytes.show()
    
    logs = grouped_bytes.join(grouped_names,'hostname')
    
    n = logs.count()
    xi = grouped_names['count']
    xi2 = xi*xi
    yi = grouped_bytes['sum(bytes)']
    yi2 = yi*yi
    xiyi = xi*yi
    
    logs = logs.withColumn('xi', xi)
    logs = logs.withColumn('xi2', xi2)
    logs = logs.withColumn('yi', yi)
    logs = logs.withColumn('yi2', yi2)
    logs = logs.withColumn('xiyi', xiyi)
    #logs.show()
    
    #referred to https://stackoverflow.com/questions/47812526/pyspark-sum-a-column-in-dataframe-and-return-results-as-int
    xi = logs.agg(functions.sum('xi')).collect()[0][0]
    yi = logs.agg(functions.sum('yi')).collect()[0][0]
    xi2 = logs.agg(functions.sum('xi2')).collect()[0][0]
    yi2 = logs.agg(functions.sum('yi2')).collect()[0][0]
    xiyi = logs.agg(functions.sum('xiyi')).collect()[0][0]
    
    numerator = (n * xiyi) - (xi*yi)
    
    dnom1 = (n * xi2) - (xi * xi)
    dnom1 = math.sqrt(dnom1) 
    dnom2 = (n* yi2) - (yi*yi)
    dnom2 = math.sqrt(dnom2)
    
    denominator = dnom1 * dnom2
    
    r = numerator/ denominator
    
    

    #r = 0 # TODO: it isn't zero.
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)

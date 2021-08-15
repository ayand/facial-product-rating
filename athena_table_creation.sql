CREATE EXTERNAL TABLE `facialratings`(
  `id` string,
  `productid` string,
  `userid` string,
  `emotion` string,
  `gender` string,
  `age` int,
  `timestamp` timestamp)
PARTITIONED BY (
  `year` int,
  `month` int,
  `day` int)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://(SUBSTITUTE NAME OF ANALYTICS BUCKET HERE)/facialratingsdata'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'transient_lastDdlTime'='1628998097');

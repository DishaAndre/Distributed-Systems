# Word Count using Hadoop

## How to Run

### 1. Start Hadoop HDFS

```bash
start-dfs.sh
```

Check that Hadoop services are running:

```bash
jps
```

### 2. Create HDFS Input Directory

```bash
hdfs dfs -mkdir -p /wordcount/input
```

### 3. Upload Input File to HDFS

```bash
hdfs dfs -put input.txt /wordcount/input/
```

### 4. Run the Hadoop MapReduce Program

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar \
-input /wordcount/input \
-output /wordcount/output \
-mapper mapper.py \
-reducer reducer.py \
-file mapper.py \
-file reducer.py
```

### 5. View the Output

```bash
hdfs dfs -cat /wordcount/output/part-00000
```

The output contains the frequency of each word in the input file.

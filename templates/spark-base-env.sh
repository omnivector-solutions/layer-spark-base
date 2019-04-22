export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre

export SPARK_HOME=${SPARK_HOME:-/opt/spark}
export SPARK_LOG_DIR=${SPARK_LOG_DIR:-/var/log/spark}
export SPARK_LOCAL_DIRS=${SPARK_LOCAL_DIRS}:-/srv/spark_local
export SPARK_WORKER_DIR=/srv/spark_work

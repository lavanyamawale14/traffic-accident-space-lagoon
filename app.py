
from flask import Flask, render_template
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, desc, to_date, year, col

app = Flask(__name__)

# Read the accident dataset directly from Hadoop HDFS
DATASET_PATH = "hdfs://localhost:9000/traffic_accident/indian_roads_dataset.csv"


# Run Spark analysis once and reuse the results
def load_dashboard_data():

    spark = (
        SparkSession.builder
        .appName("Indian Road Accident Dashboard")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    df = spark.read.csv(
        DATASET_PATH,
        header=True,
        inferSchema=True
    )

    total_accidents = df.count()

    severity = [
        {
            "name": row["accident_severity"],
            "count": row["total"]
        }
        for row in (
            df.groupBy("accident_severity")
            .agg(count("*").alias("total"))
            .orderBy(desc("total"))
            .collect()
        )
    ]

    states = [
        {
            "name": row["state"],
            "count": row["total"]
        }
        for row in (
            df.groupBy("state")
            .agg(count("*").alias("total"))
            .orderBy(desc("total"))
            .collect()
        )
    ]

    weather = [
        {
            "name": row["weather"],
            "count": row["total"]
        }
        for row in (
            df.groupBy("weather")
            .agg(count("*").alias("total"))
            .orderBy(desc("total"))
            .collect()
        )
    ]

    hotspots = [
        {
            "city": row["city"],
            "state": row["state"],
            "count": row["total"]
        }
        for row in (
            df.groupBy("city", "state")
            .agg(count("*").alias("total"))
            .orderBy(desc("total"))
            .limit(10)
            .collect()
        )
    ]

    return {
        "total_accidents": total_accidents,
        "severity": severity,
        "states": states,
        "weather": weather,
        "hotspots": hotspots
    }


# Cache results so Spark doesn't run on every page refresh
dashboard_data = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    global dashboard_data

    if dashboard_data is None:
        dashboard_data = load_dashboard_data()

    return render_template(
        "dashboard.html",
        data=dashboard_data
    )


# ADVANCED APACHE SPARK ANALYSIS
def load_analysis_data():

    spark = (
        SparkSession.builder
        .appName("Indian Road Accident Dashboard")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    df = spark.read.csv(
        str(DATASET_PATH),
        header=True,
        inferSchema=True
    )

    # Dates in our dataset use DD-MM-YYYY
    df = df.withColumn(
        "accident_date",
        to_date(col("date"), "dd-MM-yyyy")
    )

    def grouped_counts(column_name):
        return [
            {
                "name": str(row[column_name]),
                "count": row["total"]
            }
            for row in (
                df.groupBy(column_name)
                .agg(count("*").alias("total"))
                .orderBy(desc("total"))
                .collect()
            )
        ]

    yearly = [
        {"name": str(row["year"]), "count": row["total"]}
        for row in (
            df.filter(col("accident_date").isNotNull())
            .withColumn("year", year(col("accident_date")))
            .groupBy("year")
            .agg(count("*").alias("total"))
            .orderBy("year")
            .collect()
        )
    ]

    hourly = [
        {"name": str(row["hour"]), "count": row["total"]}
        for row in (
            df.groupBy("hour")
            .agg(count("*").alias("total"))
            .orderBy("hour")
            .collect()
        )
    ]

    severity_by_road = [
        {
            "road_type": row["road_type"],
            "severity": row["accident_severity"],
            "count": row["total"]
        }
        for row in (
            df.groupBy("road_type", "accident_severity")
            .agg(count("*").alias("total"))
            .orderBy("road_type", "accident_severity")
            .collect()
        )
    ]

    return {
        "yearly": yearly,
        "hourly": hourly,
        "causes": grouped_counts("cause"),
        "road_types": grouped_counts("road_type"),
        "weekdays": grouped_counts("day_of_week"),
        "severity_by_road": severity_by_road,
        "invalid_dates": df.filter(
            col("accident_date").isNull()
        ).count()
    }


analysis_data = None



@app.route("/analysis")
def analysis():
    global analysis_data

    if analysis_data is None:
        analysis_data = load_analysis_data()

    return render_template(
        "analysis.html",
        data=analysis_data
    )



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

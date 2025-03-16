## Ý tưởng tổng quan

Việc thêm Docker vào dự án CarInsight sẽ mang lại nhiều lợi ích như:

- Đảm bảo môi trường phát triển và sản xuất nhất quán

- Dễ dàng triển khai và mở rộng

- Quản lý các dependencies hiệu quả

- Giảm thiểu vấn đề "works on my machine"

- Tạo điều kiện thuận lợi cho CI/CD

Tôi đề xuất xây dựng một giải pháp Docker Compose với nhiều container riêng biệt cho từng thành phần, kết nối thông qua mạng Docker.
 
version: '3.8'

services:
  # Cơ sở dữ liệu
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: Kkagiuma2004@
      POSTGRES_DB: DataWarehouse
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init_scripts:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    networks:
      - car_insight_network

  # Apache Hadoop HDFS
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: namenode
    volumes:
      - hadoop_namenode:/hadoop/dfs/name
    environment:
      - CLUSTER_NAME=car_insight_hadoop
    env_file:
      - ./hadoop.env
    ports:
      - "9870:9870"
      - "9000:9000"
    networks:
      - car_insight_network

  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode
    volumes:
      - hadoop_datanode:/hadoop/dfs/data
    env_file:
      - ./hadoop.env
    depends_on:
      - namenode
    networks:
      - car_insight_network

  # Apache Kafka và Zookeeper
  zookeeper:
    image: wurstmeister/zookeeper:3.4.6
    ports:
      - "2181:2181"
    networks:
      - car_insight_network

  kafka:
    image: wurstmeister/kafka:2.13-2.7.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka
      KAFKA_CREATE_TOPICS: "new-data-topic:1:1,new-warehouse-data:1:1"
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - car_insight_network

  # Apache Airflow
  airflow:
    build:
      context: .
      dockerfile: ./docker/airflow/Dockerfile
    depends_on:
      - postgres
      - kafka
    volumes:
      - ./dags:/opt/airflow/dags
      - ./scripts:/opt/airflow/scripts
      - ./logs:/opt/airflow/logs
    ports:
      - "8080:8080"
    networks:
      - car_insight_network

  # Streamlit App
  streamlit:
    build:
      context: .
      dockerfile: ./docker/streamlit/Dockerfile
    depends_on:
      - postgres
    ports:
      - "8501:8501"
    volumes:
      - ./my_streamlit_app:/app
    networks:
      - car_insight_network

  # Crawler và ETL Service
  data_services:
    build:
      context: .
      dockerfile: ./docker/data_services/Dockerfile
    depends_on:
      - postgres
      - namenode
      - kafka
    volumes:
      - ./scripts:/app/scripts
      - ./data_crawled:/app/data_crawled
      - ./json_output:/app/json_output
    networks:
      - car_insight_network

networks:
  car_insight_network:
    driver: bridge

volumes:
  postgres_data:
  hadoop_namenode:
  hadoop_datanode:
# WSB_SBD_2026Z

`docker-compose up -d`

`docker exec -it spark-iceberg bash`

`python3 /home/iceberg/demo.py`

lub

http://localhost:8888

notatnik: local_demo/demo.ipynb


volumes:
      - ./demo.py:/home/iceberg/demo.py
      - ./warehouse:/home/iceberg/warehouse
      - ./notebooks:/home/iceberg/notebooks/local_demo


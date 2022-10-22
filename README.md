1. Install docker and docker-compose
1. Set up mongo and mongo express containers by running `docker-compose up -d` (or `docker compose up -d`, depending on your compose version)
1. Create test databases by running `python3 create_db.py`
1. Run the tests by running `python3 test.py`

- You can manually inspect the db through web by going to `http://localhost:8081`  
- Database naming convention is `shop-<number of products>-<number of instances/variants per product>

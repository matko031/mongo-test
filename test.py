from pymongo import MongoClient
import time


def get_random_products(col, n):
    start = time.time()
    res = col.aggregate(
            [ 
                { "$sample": { "size": n } },
                { "$project": { "_id": 0, "name": 1, "type": 1, "brand": 1} }
                ]
            )
    end = time.time()
    print(f"Fetched {n} random products in {end-start} seconds")


def get_products_by_color(products_col, instances_col, color):
    start = time.time()
    product_ids = instances_col.distinct("product_id", {"color": color})
    products = products_col.find({"_id": {"$in": product_ids}} )
    end = time.time()
    print(f"Fetched all products of {color} color in {end-start} seconds")

def get_all_types_in_price_range(products_col, instances_col, typ, price_low, price_high):
    start = time.time()
    instance_ids = list(products_col.aggregate( 
            [
                {"$match": {"type": typ}},
                {"$project": {"instances": 1}},
                {"$unwind": "$instances"},
                {"$group": {"_id": "null", "instances": {"$push": "$instances"}}},
                {"$project": {"_id": 0, "instances": 1}}
            ]
        ))

    if len(instance_ids) == 0:
        print(f"No products of type {typ} found")

    else:
        end1 = time.time()
        print(f"Found products of type {typ} in {end1-start}")

        instance_ids = instance_ids[0]["instances"]
        product_ids = list(instances_col.aggregate( 
                [
                    {"$match": {
                        "_id": {"$in": instance_ids}, 
                        "price": {"$gt": price_low, "$lt": price_high} 
                        }
                    },
                    {"$group": {"_id": "null", "product_ids": {"$addToSet": "$product_id"}}},
                    {"$project": {"_id":0, "product_ids": 1}},
                ]))


        if len(product_ids) == 0:
            print(f"No products of type {typ} found with price between {price_low} and {price_high} found")

        else:
            end2 = time.time()
            print(f"Found product ids with price between {price_low} and {price_high} in {end2-end1} seconds")

            product_ids = product_ids[0]["product_ids"]            
            products = products_col.find({"_id": {"$in": product_ids}})

            end3 = time.time()
            print(f"Found products of type {typ} and price between {price_low} and {price_high} in {end3-end2} seconds")
            print(f"Total: {end3-start}")


if __name__ == "__main__":

    CONNECTION_STRING = "mongodb://root:example@localhost"
 
    client = MongoClient(CONNECTION_STRING)

    dbs = ["shop-10-3", "shop-1000-3000", "shop-10000-30", "shop-10000-300"]
    for db in dbs:
        print(db)
        print("-------------------------------\n")
        db = client[db]
        products_col = db["products"]
        instances_col = db["instances"]

        get_random_products(products_col, 1)
        print("")
        get_random_products(products_col, 20)
        print("")
        get_random_products(products_col, 200)
        print("")
        print("")

        get_products_by_color(products_col, instances_col, "yellow")
        print("")
        get_products_by_color(products_col, instances_col, "red")
        print("")
        get_products_by_color(products_col, instances_col, "blue")
        print("")
        print("")

        get_all_types_in_price_range(products_col, instances_col, "jacket", 5, 380)
        print("")
        get_all_types_in_price_range(products_col, instances_col, "jacket", 20, 40)
        print("")
        get_all_types_in_price_range(products_col, instances_col, "jacket", 30, 40)
        print("====================================================================\n")

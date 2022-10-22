from pymongo import MongoClient
import random



def get_random_name(n=1):

    words = ['penticle', 'rabbinical', 'renversement', 'cementer', 'perivesical', 'niched', 'ochotonidae', 'suer', 'overaffected', 'coalifying', 'scalation', 'motivating', 'marrella', 'we', 'throwdown', 'marmennill', 'angiography', 'rhopalism', 'gainspeaker', 'dialyzable', 'properly', 'incubating', 'dimerous', 'buccal', 'thorium', 'coadapting', 'opiane', 'describer', 'unalmsed', 'propretorial', 'heterocerous', 'yows', 'bisellium', 'marishness', 'standbybys', 'alliaceous', 'inculcate', 'preluxurious', 'uncountable', 'reoffers', 'bobac', 'berrypicker', 'potboils', 'palaeobiological', 'recoiner', 'overdiscriminating', 'phonopore', 'exudates', 'gargantua', 'mythologies', 'glopnen', 'spurted', 'barns', 'decalcified', 'disenchantment', 'incidentals', 'vanload', 'liquamen', 'ribonucleotide', 'summarise', 'clobber', 'nonstatic', 'caricographer', 'vitrobasalt', 'prologuising', 'hansardization', 'pecks', 'esoterics', 'unspringing', 'hetairy', 'medicomechanical', 'trailside', 'myeloganglitis', 'galluses', 'dutchman', 'christianomastix', 'squareman', 'ablated', 'galvayned', 'faeroe', 'acrodus', 'reliction', 'burgraves', 'restep', 'lubricous', 'multimacular', 'abdominocardiac', 'antennular', 'antebath', 'eyeleted', 'thermionics', 'anisocarpic', 'briseis', 'awhirl', 'lughdoan', 'aumbries', 'zapateados', 'arachnopia', 'acater', 'heroize']

    name = ""
    for i in range(n-1):
        name += words[random.randint(0, len(words)-1)] + " "
    name += words[random.randint(0, len(words)-1)]
    return name

def get_random_brand():
    brands = ['creta', 'attatched', 'violetish', 'aggrieves', 'timpanum', 'detonability', 'tetrao', 'isopelletierin', 'haznadar', 'semolinas', 'unvoluntarily', 'souchy', 'pneumonographic', 'ungarnish', 'cash', 'minutissimic', 'backwoodsmen', 'kermanji', 'barmbrack', 'auxanogram']

    return brands[random.randint(0, len(brands)-1)]

def create_products(col, nb_products):
    products = []

    types = ["jacket", "tshirt", "pants", "socks"]

    for i in range(nb_products):
        print(f"Creating product {i+1} / {nb_products}", end="\r")
        item = {
                "type": types[random.randint(0,3)],
                "name": get_random_name(3),
                "brand": get_random_brand(),
                "instances": []
                }
        products.append(item)

    print("")

    res = col.insert_many(products)
    return res.inserted_ids


def create_instances(inst_col, product_ids, instances_per_product):

    sizes = ["xs", "s", "m", "l", "xl", "xxl"]
    colors = ["yellow", "blue", "red", "brown", "appelblauwzeegroen", "orange", "black", "white", "purple"]
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    instances = []
    for i in range(len(product_ids)): 

        id = product_ids[i]

        for j in range(instances_per_product):

            print(f"Creating instance {j+1} / {instances_per_product} for product {i+1} / {len(product_ids)}", end="\r")

            instance = {
                        "product_id": id,
                        "size": sizes[random.randint(0, len(sizes)-1)], 
                        "color": colors[random.randint(0, len(colors)-1)], 
                        "quantity": random.randint(0, 200), 
                        "provider": letters[random.randint(0, len(letters)-1)],
                        "price": random.randint(15, 200) 
                    }
            instances.append(instance)
   
    print("")

    print("Inserting instances in db")
    res = inst_col.insert_many(instances)
    print("Done inserting instances in db")

    return res.inserted_ids

def update_products(products_col, product_ids, instances_ids, instances_per_product):

    for i, id in enumerate(product_ids):
        print(f"Updating product {i+1}", end="\r")
        update_query = {"_id": id}
        newvalues = { "$set": { "instances": instances_ids[i*instances_per_product:(i+1)*instances_per_product]} }

        products_col.update_one(update_query, newvalues)
    print("")


def create_db(client, db_name, nb_products, instances_per_product):

    print(f"Creating database {db_name}")
    client.drop_database(db_name)
    db = client[db_name]
    products_col = db["products"]
    instances_col = db["instances"]

    product_ids = create_products(products_col, nb_products)

    instances_ids = create_instances(instances_col, product_ids, instances_per_product) 

    update_products(products_col, product_ids, instances_ids, instances_per_product)
    print("")

if __name__ == "__main__":   

    CONNECTION_STRING = "mongodb://root:example@localhost"
 
    client = MongoClient(CONNECTION_STRING)

    #create_db(client, "shop-10-3", 10, 3)
    #create_db(client, "shop-1000-3000", 1000, 3000)
    #create_db(client, "shop-10000-30", 10000, 30)
    create_db(client, "shop-10000-300", 10000, 300)

    # These two were two big for my machine, I ran out of RAM trying to insert them
    #create_db(client, "shop-1000-30000", 1000, 30000)
    #create_db(client, "shop-10000-30000", 10000, 30000)



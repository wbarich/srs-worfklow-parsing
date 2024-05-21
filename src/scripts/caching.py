import pickle

def dump_cache(cache):
    with open('cache.pkl', 'wb') as f:
        pickle.dump(cache, f)

def retrieve_cache():
    try:
        with open('cache.pkl', 'rb') as f:
            loaded_cache = pickle.load(f)
        print("Loaded cache from disk")
    except:
        print("Not loading cache as it does not exist")
        return {}
    return loaded_cache

def check_cache(query, cache):
    if query in cache:
        return True
    else:
        return False
from cachepy import cachepy
    
if __name__ == "__main__":
    #No need to put a \n
    print ''
    stats = cachepy.stats()
    cache_memory_address = stats['cache_memory_address']
    del stats['cache_memory_address']
    print cache_memory_address, stats
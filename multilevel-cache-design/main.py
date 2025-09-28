from multilevel_cache import MultiLevelCache

if __name__ == "__main__":
    capacities = [2, 3, 4]
    cache = MultiLevelCache(max_levels=3, capacities=capacities)

    cache.write("a", "1")
    cache.write("b", "2")
    cache.write("c", "3")
    print(cache)

    print("Read b:", cache.read("b"))
    print(cache)

    cache.delete("a")
    print(cache)

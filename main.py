import memcache
mc = memcache.Client(['188.134.82.95:7005'], debug=0)
mc.set("default_message", "Hello World!")
print(mc.get("default_message"))

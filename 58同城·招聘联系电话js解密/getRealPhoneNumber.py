import execjs

js = execjs.compile(open("js.js", "r").read())
token = "EteFNAJt19Y7/qQuQIhDvlMNBD2PGpoWvoGEmqZm4xE="
realPhone = js.call("getRealPhone", token)
print(realPhone)
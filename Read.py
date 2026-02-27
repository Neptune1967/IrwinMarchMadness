import http.client

conn = http.client.HTTPSConnection("march-madness2.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "b3c5ee02femsh8be036e9d709a1bp1da04ejsn93c6f4e84eac",
    'x-rapidapi-host': "march-madness2.p.rapidapi.com"
}

conn.request("GET", "/matchups/2025?teamA=Nort%20Carolina&teamB=San%20Diego%20State", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

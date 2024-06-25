import requests
import json

#functions
def ziptogps(zipcode):
    urltemp="https://atlas.microsoft.com/search/address/json?&subscription-key=9PgKvPbHvFf24jvGx59raLySDaE7USdox8rWgowue7yUNCbuLvVDJQQJ99AFACYeBjFvS6NiAAAgAZMPFmFd&api-version=1.0&language=en-US&query="+str(zipcode)+",USA"
    response1 = requests.get(urltemp)
    if response1.status_code == 200:
        data1 = response1.json()
        return float(data1['results'][0]['position']['lat']),float(data1['results'][0]['position']['lon'])
    
def minfinder(warehouselocs):
    minfunlat=100000
    minfunlon=100000
    for i in range(0,len(warehouselocs)):
        if warehouselocs[i][0]<minfunlat:
            minfunlat=warehouselocs[i][0]
    for j in range(0,len(warehouselocs)):
        if warehouselocs[j][1]<minfunlon:
            minfunlon=warehouselocs[j][1]
    return minfunlat,minfunlon

def maxfinder(warehouselocsmax):
    maxfunlat=-100000
    maxfunlon=-100000
    for a in range(0,len(warehouselocsmax)):
        if warehouselocsmax[a][0]>maxfunlat:
            maxfunlat=warehouselocsmax[a][0]
    for b in range(0,len(warehouselocsmax)):
        if warehouselocsmax[b][1]>maxfunlon:
            maxfunlon=warehouselocsmax[b][1]
    return maxfunlat,maxfunlon

def distancefinder(lat1, lat2, long1, long2):
    url = "https://atlas.microsoft.com/route/directions/json?api-version=1.0&dataFormat=zip&subscription-key=9PgKvPbHvFf24jvGx59raLySDaE7USdox8rWgowue7yUNCbuLvVDJQQJ99AFACYeBjFvS6NiAAAgAZMPFmFd&query="+lat1+","+long1+":"+lat2+","+long2+"&report=effectiveSettings"
    response=requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['routes'][0]['summary']['lengthInMeters']
    else:
        return "np"
    
def gpstozip(latx1, lonx1):
    url = "https://atlas.microsoft.com/search/address/reverse/json?api-version=1.0&subscription-key=9PgKvPbHvFf24jvGx59raLySDaE7USdox8rWgowue7yUNCbuLvVDJQQJ99AFACYeBjFvS6NiAAAgAZMPFmFd&query="+str(latx1)+","+str(lonx1)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['addresses'][0]['address']['postalCode']
    else:
        print(data)






#main code
zipcodeslibrary = []
warehouselocations = []
testvar1="n/a"
while testvar1!="":
    testvar1 = input("Enter a zip code or press enter:")
    if testvar1!="":
        zipcodeslibrary.append(testvar1)
for m in range(0, len(zipcodeslibrary)):
    templa1 , templo1 = ziptogps(zipcodeslibrary[m])
    templist1 = [templa1, templo1]
    warehouselocations.append(templist1)


listminlat, listminlon = minfinder(warehouselocations)
listmaxlat, listmaxlon = maxfinder(warehouselocations)

latdiff = listmaxlat-listminlat
londiff = listmaxlon-listminlon
numofattempts = latdiff*londiff*len(warehouselocations)
print(numofattempts)

finaldisl1=1000000000
finallatl1=0
finallonl1=0

for x in range(0, int(londiff)):
    for y in range(0,int(latdiff)):
        tempdistance=0
        for z in range(0,len(warehouselocations)):
            tempvar1=distancefinder(str(listminlat+y), str(warehouselocations[z][0]), str(listminlon+x),str(warehouselocations[z][1]))
            if tempvar1=="np":
                continue
            else:
                tempdistance+=int(tempvar1)
        if tempdistance<finaldisl1 and tempdistance!=0:
            finaldisl1=tempdistance
            finallatl1=listminlat+y
            finallonl1=listminlon+x
for x1 in range(0, 10):
    for y1 in range(0, 10):
        for z in range(0, len(warehouselocations)):
            tempvar1=distancefinder(str(finallatl1+(y1*0.1)), str(warehouselocations[z][0]), str(finallonl1+(x1*0.1)),str(warehouselocations[z][1]))
            if tempvar1=="np":
                continue
            else:
                tempdistance+=int(tempvar1)
        if tempdistance<finaldisl1 and tempdistance!=0:
            finaldisl1=tempdistance
            finallatl1=listminlat+y
            finallonl1=listminlon+x


print(gpstozip(finallatl1,finallonl1))
print(finaldisl1)
print(str(finallatl1)+','+str(finallonl1))



    



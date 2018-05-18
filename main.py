from htmlConverter import AdvertisementEntry, AdvertisementList


advertisements = AdvertisementList()
advertisements.fillWithFirstJobs(requestedJobs=2)
print(advertisements.stringifyAllResults())
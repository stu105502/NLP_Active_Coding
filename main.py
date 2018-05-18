from htmlConverter import AdvertisementEntry, AdvertisementList


advertisements = AdvertisementList()
advertisements.fillWithFirstJobs(requestedJobs=100)
csv = advertisements.convertEntriesToCSV()
fileHandler = open("results.csv", "w")
fileHandler.write(csv)
fileHandler.close()
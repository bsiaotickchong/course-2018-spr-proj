import urllib.request
import json
import dml
import prov.model
import datetime
import uuid


class parkingData(dml.Algorithm):
    contributor = 'aoconno8_dmak1112'
    reads = []
    writes = ['aoconno8_dmak1112.parkingData']

    @staticmethod
    def execute(trial=False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aoconno8_dmak1112', 'aoconno8_dmak1112')

        url = 'https://data.boston.gov/api/3/action/datastore_search?resource_id=8d38cc9d-8c58-462e-b2df-b793e9c05612&limit=572'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        parking_json = [json.loads(response)]
        repo.dropCollection("parkingData")
        repo.createCollection("parkingData")
        repo['aoconno8_dmak1112.parkingData'].insert_many(parking_json)
        repo['aoconno8_dmak1112.parkingData'].metadata({'complete': True})
        print(repo['aoconno8_dmak1112.parkingData'].metadata())

        repo.logout()

        endTime = datetime.datetime.now()

        return {"start": startTime, "end": endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
        pass
        # '''
        #     Create the provenance document describing everything happening
        #     in this script. Each run of the script will generate a new
        #     document describing that invocation event.
        #     '''
        #
        # # Set up the database connection.
        # client = dml.pymongo.MongoClient()
        # repo = client.repo
        # repo.authenticate('alice_bob', 'alice_bob')
        # doc.add_namespace('alg', 'http://datamechanics.io/algorithm/')  # The scripts are in <folder>#<filename> format.
        # doc.add_namespace('dat', 'http://datamechanics.io/data/')  # The data sets are in <user>#<collection> format.
        # doc.add_namespace('ont',
        #                   'http://datamechanics.io/ontology#')  # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        # doc.add_namespace('log', 'http://datamechanics.io/log/')  # The event log.
        # doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        #
        # this_script = doc.agent('alg:alice_bob#example',
        #                         {prov.model.PROV_TYPE: prov.model.PROV['SoftwareAgent'], 'ont:Extension': 'py'})
        # resource = doc.entity('bdp:wc8w-nujj',
        #                       {'prov:label': '311, Service Requests', prov.model.PROV_TYPE: 'ont:DataResource',
        #                        'ont:Extension': 'json'})
        # get_found = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        # get_lost = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        # doc.wasAssociatedWith(get_found, this_script)
        # doc.wasAssociatedWith(get_lost, this_script)
        # doc.usage(get_found, resource, startTime, None,
        #           {prov.model.PROV_TYPE: 'ont:Retrieval',
        #            'ont:Query': '?type=Animal+Found&$select=type,latitude,longitude,OPEN_DT'
        #            }
        #           )
        # doc.usage(get_lost, resource, startTime, None,
        #           {prov.model.PROV_TYPE: 'ont:Retrieval',
        #            'ont:Query': '?type=Animal+Lost&$select=type,latitude,longitude,OPEN_DT'
        #            }
        #           )
        #
        # lost = doc.entity('dat:alice_bob#lost',
        #                   {prov.model.PROV_LABEL: 'Animals Lost', prov.model.PROV_TYPE: 'ont:DataSet'})
        # doc.wasAttributedTo(lost, this_script)
        # doc.wasGeneratedBy(lost, get_lost, endTime)
        # doc.wasDerivedFrom(lost, resource, get_lost, get_lost, get_lost)
        #
        # found = doc.entity('dat:alice_bob#found',
        #                    {prov.model.PROV_LABEL: 'Animals Found', prov.model.PROV_TYPE: 'ont:DataSet'})
        # doc.wasAttributedTo(found, this_script)
        # doc.wasGeneratedBy(found, get_found, endTime)
        # doc.wasDerivedFrom(found, resource, get_found, get_found, get_found)
        #
        # repo.logout()
        #
        # return doc


parkingData.execute()
# doc = example.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
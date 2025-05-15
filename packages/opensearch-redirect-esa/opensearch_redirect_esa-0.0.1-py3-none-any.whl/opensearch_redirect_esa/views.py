from django.views import View
from django.views.generic import FormView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import requests
import xmltodict
from elasticsearch import Elasticsearch

class BasicJSONView(View):
    
    def get(self, request, uuid):
        print(uuid)
        return JsonResponse(
            requests.get(f'https://catalogue.ceda.ac.uk/api/v2/observations.json?uuid={uuid}').json()
        )

class BasicHTMLView(FormView):
    template_name = 'base.html'

    def get(self, request, uuid):

        resp = requests.get(f'https://catalogue.ceda.ac.uk/api/v2/observations.json?uuid={uuid}').json()['results'][0]

        # Elasticsearch query
        cli = Elasticsearch(hosts=['https://elasticsearch.ceda.ac.uk'])

        opensearch = cli.search(
            index='opensearch-collections',
            body={
                "query":{
                    "bool": {
                    "must":[
                        {
                        "match":{
                            "collection_id":uuid
                        }
                        }
                    ]
                    }
                }
            })
        
        print(resp)
        
        resp['start_date'] = opensearch['hits']['hits'][0]['_source']['start_date'].split('T')[0]
        resp['end_date'] = opensearch['hits']['hits'][0]['_source']['end_date'].split('T')[0]

        # Date time range (formatted to just days)
        # Number of files
        # Catalogue size
        # Link to MOLES - Dataset Information
        resp['catalog_link'] = 'https://google.com'
        resp['catalog_size'] = '1.0 B'
        resp['num_files'] = '4000'


        #resp2 = requests.get(f'http://archive-opensearch.164.30.69.113.nip.io/opensearch/request?parentIdentifier={uuid}&httpAccept=application/geo%2Bjson')

        #print(resp2.json())
        #html_template = html_template.replace('$abstract$',context['abstract'])
        #html_template = html_template.replace('$title$',context['title'])

        # Info ['ob_id', 'uuid', 'title', 'abstract', 'keywords', 'publicationState', 
        # 'dataPublishedTime', 'doiPublishedTime', 'updateFrequency', 'status', 
        # 'result_field', 'timePeriod', 'geographicExtent', 'nonGeographicFlag', 
        # 'phenomena', 'dataLineage', 'removedDataTime', 'removedDataReason', 'language', 
        # 'identifier_set', 'projects', 'observationcollection_set', 'responsiblepartyinfo_set', 
        # 'procedureAcquisition', 'procedureCompositeProcess', 'procedureComputation'])

        resp['esa_desc'] = 'ESA Description - Source Unknown'

        return render(request, "base.html", resp)
import copy 
import re
from datetime import datetime, timedelta
from rdflib import Graph
import rdflib

def make_rig(rdg, mapping_values):
    rdg_copy = copy.deepcopy(rdg)
    mapping_section = rdg.split('sswap:hasMapping [')[1].split(']')[0].split("sswap:mapsTo")[0]
    mapping_section_prev = copy.copy(mapping_section)
    
    for key, value in mapping_values.items():
        print(key,value)
        mapping_section = re.sub(f'{key} ""', f'{key} "{value}"', mapping_section)

    rig = rdg_copy.replace(mapping_section_prev,mapping_section)
    
    return rig

def rdf_query(name,places,bedrooms,lakedist,city,citydist,bookingday,ndays,maxshift):
    date_object = datetime.strptime(bookingday, "%Y-%m-%d")
    # Add the days
    new_date_object = date_object + timedelta(days=ndays)

    # Convert back to string if needed
    bookingendday = new_date_object.strftime("%Y-%m-%d")
    print(bookingday,bookingendday)
    g = Graph()
    g.parse("cottage_instance.rdf", format="turtle")
    print(g)
    que = f"""
    PREFIX cot: <http://users.jyu.fi/~mihossai/cottages.owl>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?cottageName ?cottageAddress ?cottageImage ?bookingStartDate ?bookingEndDate 
    WHERE {{
        ?cottage a cot:Cottage .
        ?cottage cot:hasName ?cottageName .
        ?cottage cot:hasAddress ?cottageAddress .
        ?cottage cot:hasImage ?cottageImage .
        ?cottage cot:hasPlaces ?actualCapacity .
        ?cottage cot:hasBedrooms ?actualBedrooms .
        ?cottage cot:distanceToLake ?actualLakeDistance .
        ?cottage cot:nearestCity ?nearestCity .
        ?cottage cot:distanceToCity ?actualCityDistance .
        ?cottage cot:bookingStartDate ?bookingStartDate .
        ?cottage cot:bookingEndDate ?bookingEndDate .
        
        FILTER (?bookingStartDate > '{bookingendday}' || ?bookingEndDate < '{bookingday}').
        FILTER (?actualCapacity >= {places}).
        FILTER (?actualBedrooms >= {bedrooms}).
        FILTER (?actualLakeDistance <= {lakedist}).
        FILTER (?nearestCity = '{city}').
        FILTER (?actualCityDistance <= {citydist}).
    }}
"""

    print(que)
    results = g.query(que)
    return results,bookingendday

def get_rdg_properties(turtle_file):
    g = rdflib.Graph()

    # turtle_file = 'static/turtle_files/RDG.ttl'
    g.parse(turtle_file, format='turtle')

    # Find hasMapping
    for subject, predicate, object in g:
        # Convert subject, predicate, object to strings for easier handling
        subj_str = str(subject)
        pred_str = str(predicate)
        obj_str = str(object)
        if pred_str.split("/")[-1]=="hasMapping":
            hasMapping_Sub = obj_str
        # print("hello",subj_str,"--",pred_str,"--",obj_str)
    properties = []
    for subject, predicate, object in g:
        # Convert subject, predicate, object to strings for easier handling
        subj_str = str(subject)
        pred_str = str(predicate)
        obj_str = str(object)
        if subj_str == hasMapping_Sub and obj_str=='':
            print("helo",subj_str,"---",pred_str,"--",obj_str)
            properties.append(pred_str.split('/')[-1])
        
    return properties
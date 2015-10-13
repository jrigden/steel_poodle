import json
import os.path
from pelican import signals



def write_geojson(gen, writer):
    siteurl = writer.settings.get('SITEURL')
    FeatureCollection = {}
    FeatureCollection['type'] = "FeatureCollection"
    FeatureCollection['features'] = []
    FeatureCollection['tags'] = set()
    for article in gen.articles:
        if (hasattr(article, 'longitude') and hasattr(article, 'latitude')):
            Feature = {}
            Feature['type'] = "Feature"
            Feature['geometry'] = {}
            Feature['geometry']['type'] = "Point"
            Feature['geometry']['coordinates'] = (float(article.longitude),float(article.latitude))
            Feature['properties'] = {}
            Feature['properties']['title'] = article.title
            Feature['properties']['url'] = siteurl + '/' + article.url
            Feature['properties']['summary'] = article.summary
            FeatureCollection['features'].append(Feature)
            for tag in article.tags:
                FeatureCollection['tags'].add(tag.url)
    FeatureCollection['tags'] = list(FeatureCollection['tags'])
    json_path = os.path.join(writer.output_path, 'geo.json')
    with open(json_path, 'w') as outfile:
        json.dump(FeatureCollection, outfile)



def register():
    signals.article_writer_finalized.connect(write_geojson)

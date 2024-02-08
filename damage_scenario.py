import xml.etree.ElementTree as ET 
import pandas as pd

def xsam_to_excel_converter(path):
        tree = ET.parse(path)

        root = tree.getroot()


        #module 1 component dictionary
        component_dictionary = {}

        subcomponent_node = root.find(".//{http://www.security-analyst.org/xsam}SystemChunk[@name='Components']//{http://www.security-analyst.org/xsam}Elements//{http://www.security-analyst.org/xsam}Component//{http://www.security-analyst.org/xsam}SubComponents")

        for child in subcomponent_node:
            component_dictionary[child.attrib['{http://www.itemis.de/mps}id']] = child.attrib['title']





        #module 2 array of dict with title id and ratings
        array_of_dict = []

        element_node = root.find(".//{http://www.security-analyst.org/xsam}SecurityChunk[@name='Damage Scenarios']//{http://www.security-analyst.org/xsam}Elements")

        for scenario in element_node:
            arr = []
            diction = {}
            if 'title' in scenario.attrib:
                
                diction['title'] = scenario.attrib['title']
                
                impact_ratings = scenario.find(".//{http://www.security-analyst.org/xsam}ImpactRatings")
                for tuple in impact_ratings:
                    impact_rating = tuple.find(".//{http://www.security-analyst.org/xsam}ImpactRating//{http://www.security-analyst.org/xsam}ImpactRating")
                    rating = impact_rating.attrib.get('option')[-2:]
                    arr.append(rating)
                
                diction['rating_values'] = arr
                
                
                toee = scenario.find(".//{http://www.security-analyst.org/xsam}ConcernedAssets//{http://www.security-analyst.org/xsam}QualifiedAssetList//{http://www.security-analyst.org/xsam}QualifiedAssets//{http://www.security-analyst.org/xsam}QualifiedAsset//{http://www.security-analyst.org/xsam}Toee//{http://www.security-analyst.org/xsam}ComponentRef")
                target = toee.attrib.get('target')[-11:]
                diction['id'] = target
                
            
                array_of_dict.append(diction)
                


        unique_array_of_dict = []

        for d in array_of_dict:
            if d not in unique_array_of_dict:
                unique_array_of_dict.append(d)
                


        #module 3 combine 1 and 2
        for dicts in unique_array_of_dict:
            id = dicts['id']
            dicts['component'] = component_dictionary[id]
            del dicts['id']


        #module 4 dataframe and excel
        df = pd.DataFrame(unique_array_of_dict)

        df[['Component', 'Damage Scenario']] = df[['component', 'title']]
        df[['Safety', 'Financial', 'Operational', 'Privacy']] = pd.DataFrame(df['rating_values'].tolist())
        df = df[['Component', 'Damage Scenario', 'Safety', 'Financial', 'Operational', 'Privacy']]


        return df
    
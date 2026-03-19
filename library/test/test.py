import os
Name = 'Test'
Description = 'Generates URLs from input values.'
EntityType = 'URL'

def test_function(input_value):
    return {'value': f'https://www.{input_value}.org', 'name': Name, 'icon': os.path.join(os.path.dirname(__file__), 'test.png'), 'type': EntityType, 'properties': {'Status': 'Active', 'Secure': 'Yes', 'Description': Description}}
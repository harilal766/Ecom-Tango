import json

with open("test_data.json") as test_file:
    test_dict = json.load(test_file)
    
    amazon_excel = test_dict["report_files"]["amazon"]
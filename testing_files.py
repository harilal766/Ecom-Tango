import json

with open("test_data.json") as test_file:
    test_dict = json.load(test_file)
    
    amazon_label = test_dict["label_paths"]["amazon"]
    
    
    amazon_dict = test_dict["report_files"]["amazon"]
    amazon_excel = amazon_dict["file"]
    amazon_index = amazon_dict["index"]
    amazon_columns = amazon_dict["columns"]
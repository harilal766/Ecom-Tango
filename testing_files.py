import json, os

with open("test_data.json") as test_file:
    test_dict = json.load(test_file)
    test_folder = os.path.join(os.getcwd(),'test_files')
    
    #amazon_label = test_dict["label_paths"]["amazon"]
    amazon_label = os.path.join(test_folder,'amazon.pdf')
    
    amazon_dict = test_dict["report_files"]["amazon"]
    #amazon_excel = amazon_dict["file"]
    amazon_excel = os.path.join(test_folder,'amazon.xlsx')
    amazon_index = amazon_dict["index"]
    amazon_columns = amazon_dict["columns"]
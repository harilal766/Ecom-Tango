from datetime import datetime, timedelta
import pandas as pd, os, json
from openpyxl import load_workbook
from styleframe import StyleFrame, Styler
from label_sorter import LabelSorter


class Spreadsheet:
    def __init__(self, store, df, report_type):
        self.df = df
        self.report_type = report_type
        self.store = store
        
    def alphabet_based_indexing(self):
        pass
        
    def df_styling(self):
        try:
            borders = Styler(
                border_type='thin', 
                font_size = 11, font='calibri',
                horizontal_alignment='left', vertical_alignment='top'
            )
            first_column = self.df[
                self.df.columns[0]]; rest_columns = self.df[self.df.columns[1:]
            ]
            # width setting
            self.df.style.set_properties(subset=[first_column.name], **{'width': '1000px'})
            
        except Exception as e:
            print(e)
        else:
            return StyleFrame(self.df, styler_obj=borders)
        
    def create_index(self, columns_list):
        index_list = []
        starting_ascii = 65
        try:
            for number in range(0,len(columns_list)):
                index_list.append(
                    chr(starting_ascii + number)
                )
            return index_list
        except Exception as e:
            print(e)
            
    def create_pivot_table(self,index,other_columns):
        pivot_df = None
        try:
            if index and other_columns:
                pivot_df = self.df.pivot_table(
                    values = other_columns,
                    index = index,
                    aggfunc = 'sum', margins = True,
                    margins_name = 'Grand Total'
                )
                pivot_df = pivot_df.reset_index().rename(
                    columns={index: 'Row Labels'}
                )
            return pivot_df
        except Exception as e:
            print(e)
    
    def create_tally_table(self, report_df ,pivot_df, label_path):
        tally_df = None; filler = None
        tally_dictionaries = []; 
        try:
            if self.report_type in ("Order Report", "Return Report"):
                sorter_instance = LabelSorter(pdf_path=label_path)
                label_summary = sorter_instance.create_sorted_summary()
                products_list = list(label_summary.keys())
                
                if self.report_type == "Order Report":
                    for product, qty_dict in label_summary.items():
                        orders_list = []; tally_dictionary = {}
                        if product != 'Mixed':
                            tally_dictionary['Product'] = product
                            tally_dictionary['Orders'] = None
                            if type(qty_dict) == dict:
                                for qty, pages in sorted(list(qty_dict.items())):
                                    qty_based_order_count = len(pages)/2 if self.store.platform == "Amazon" else len(pages)
                                    orders_list.append(str(int(qty_based_order_count)))
                                    tally_dictionary[qty] = int(qty) * qty_based_order_count
                                    
                                print(f'Orders : {orders_list}')
                                tally_dictionary['Orders'] = '+'.join(orders_list)
                                    
                                if 'Mixed' in label_summary.keys():
                                    tally_dictionary['Mixed'] = None
                                    
                                tally_dictionary['Total'] = f'=sum(C2:E2)'
                                tally_dictionary['Rate'] = None
                                tally_dictionary['Amount'] = None
                                
                        else:
                            continue
                            
                        tally_dictionaries.append(tally_dictionary)
            tally_table_index = self.create_index(columns_list=list(tally_dictionary.keys()))   
            tally_df = pd.DataFrame(
                tally_dictionaries
            )
            return tally_df
        except Exception as e:
            return pd.DataFrame({"Error" : e})
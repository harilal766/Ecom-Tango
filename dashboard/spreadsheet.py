from datetime import datetime, timedelta
import pandas as pd, os, json
from openpyxl import load_workbook
from styleframe import StyleFrame, Styler
from label_sorter import LabelSorter


class Spreadsheet:
    def __init__(self, store, report_df, report_type):
        self.report_df = report_df
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
            first_column = self.report_df[
                self.report_df.columns[0]]; rest_columns = self.report_df[self.report_df.columns[1:]
            ]
            # width setting
            self.report_df.style.set_properties(subset=[first_column.name], **{'width': '1000px'})
            
        except Exception as e:
            print(e)
        else:
            return StyleFrame(self.report_df, styler_obj=borders)
        
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
                pivot_df = self.report_df.pivot_table(
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
    
    def create_tally_table(self, pivot_df, label_path):
        tally_df = None
        tally_dictionaries = []; rate_dict = {}
        try:
            if self.report_type == "Order Report":
                if not pivot_df is None:
                    print(pivot_df)
                    for index, row in pivot_df.iterrows():
                        pivot_product = row['Row Labels']                        
                        rate_dict[f'{pivot_product} '] = int(
                            row['item-price']/row['quantity']
                        )
                
                sorter_instance = LabelSorter(pdf_path=label_path)
                label_summary = sorter_instance.create_sorted_summary()
                row_count = 1; column_count = 0; column_range = []
                
                quantities = []
                for qty_summary in label_summary:
                    if type(label_summary[qty_summary]) == dict:
                        qty_dict = label_summary[qty_summary]
                        for qty, pages in qty_dict.items():
                            if qty not in quantities:
                                quantities.append(qty)
                        
                print(f'Quantities : {sorted(quantities)}')
                
                if self.report_type == "Order Report":
                    summary_items = label_summary.items()
                    for product_name, qty_dict in summary_items:
                        orders_list = []; tally_dictionary = {}
                        if product_name != 'Mixed':
                            tally_dictionary['Product Name'] = product_name
                            tally_dictionary['Orders'] = None
                            
                            if type(qty_dict) == dict:
                                column_count = len(tally_dictionary.keys())
                                for qty, pages in sorted(list(qty_dict.items())):
                                    column_count += 1
                                    if (qty == quantities[0] or qty == quantities[-1]) and not qty in column_range:
                                        column_range.append(str(column_count))
                                        
                                    qty_based_order_count = len(pages)/2 if self.store.platform == "Amazon" else len(pages)
                                    orders_list.append(str(int(qty_based_order_count)))
                                    tally_dictionary[qty] = int(qty) * qty_based_order_count
                                tally_dictionary['Orders'] = '+'.join(orders_list)
                            
                            if 'Mixed' in label_summary.keys():
                                tally_dictionary['Mixed'] = None
                                            
                            tally_dictionary['Total'] = f'=sum({column_range})'
                            tally_dictionary['Rate'] = rate_dict.get(product_name)
                            tally_dictionary['Amount'] = None 
                            
                            tally_dictionaries.append(tally_dictionary)
            else:
                print('Unsupported Report Type')              
                            
            
            tally_df = pd.DataFrame(
                tally_dictionaries
            )
        except Exception as e:
            return pd.DataFrame({"Error" : e})
        else:
            return tally_df
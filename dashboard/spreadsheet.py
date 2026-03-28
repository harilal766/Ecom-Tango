from datetime import datetime, timedelta
import pandas as pd, os, json
from openpyxl import load_workbook
from styleframe import StyleFrame, Styler
from label_sorter import LabelSorter
from pprint import pprint
import re

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
                    #print(pivot_df)
                    for index, row in pivot_df.iterrows():
                        pivot_product = re.sub(r"\s","",row['Row Labels'])                    
                        rate_dict[pivot_product] = int(
                            int(row['item-price'])/int(row['quantity'])
                        )
                        #print(rate_dict[pivot_product], pivot_product)
                
                sorter_instance = LabelSorter(pdf_path=label_path)
                label_summary = sorter_instance.create_sorted_summary()
                row_count = 1; starting_col_count = 0
                
                quantities = []
                mixed_dict = label_summary.get("Mixed",None)
                if mixed_dict:
                    mixed_summary = mixed_dict.get("summary", None)
                    # remove items to main summary that does not exist in the mixed one
                    for prod, qty_summary in mixed_summary.items():
                        mixed_total = sum(qty_summary.values())
                        if not prod in label_summary.keys():
                            label_summary[prod] = {"Mixed": mixed_total}
                        else:
                            label_summary[prod]["Mixed"] = mixed_total
                    label_summary.pop("Mixed",None)
                for qty_summary in label_summary:
                    if type(label_summary[qty_summary]) == dict:
                        qty_dict = label_summary[qty_summary]
                        for qty, pages in qty_dict.items():
                            if qty not in quantities:
                                quantities.append(qty)

                if self.report_type == "Order Report":
                    summary_items = label_summary.items()
                    for product_name, qty_dict in summary_items:
                        orders_list = [];  cell_range = []
                        
                        tally_dictionary = {}
                        # Dictionaries breakups to use in more optimised future updation 
                        if product_name != 'Mixed':
                            row_count += 1
                            tally_dictionary['Product Name'] = product_name
                            tally_dictionary['Orders'] = None
                            
                            if type(qty_dict) == dict:
                                starting_col_count = len(tally_dictionary.keys())
                                quantities = sorted(quantities)
                                for qty in quantities:
                                    if qty == quantities[0] or qty == quantities[-1]:
                                        if qty not in cell_range:
                                            if qty.isdigit():
                                                last_encountered_digit = int(qty)
                                            additional_count = last_encountered_digit if qty.isdigit() else last_encountered_digit+2
                                            cell_index = f'{chr(64 + starting_col_count + additional_count)}{row_count}'
                                            cell_range.append(cell_index)
                                    
                                    page_numbers = qty_dict.get(qty,None)
                                    if type(page_numbers) == list:
                                        order_count = int(len(page_numbers)/2 if self.store.platform == "Amazon" else len(page_numbers))
                                        piece_count = int(int(qty) * order_count)
                                        orders_list.append(str(order_count))
                                    else:
                                        piece_count = qty_dict.get(qty,None)
                                    tally_dictionary[qty] = piece_count
                                    
                                tally_dictionary['Orders'] = '+'.join(orders_list)
                            
                            tally_dictionary['Total'] = f'=sum({':'.join(cell_range)})' if len(cell_range)> 0 else f'=sum('
                            product_name = re.sub(r"\s","", product_name)
                            tally_dictionary['Rate'] = rate_dict.get(product_name,None)
                            tally_dictionary['Amount'] = None 
                            tally_dictionaries.append(tally_dictionary)
            else:
                print('Unsupported Report Type')              
                            
        except Exception as e:
            return pd.DataFrame({"Error" : e})
        else:
            tally_df = pd.DataFrame(
                tally_dictionaries
            )
            return tally_df
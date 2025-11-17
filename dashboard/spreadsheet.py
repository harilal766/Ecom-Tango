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
        pre_df = []; input_dict = {}
        try:
            if self.report_type in ("Order Report", "Return Report"):
                products_list = pivot_df['Row Labels'].to_list()
                filler = [None] * len(products_list)
                if self.report_type == "Order Report":
                    # Find quantities
                    quantity_dict = {}
                    for qty in sorted(report_df['quantity'].to_list()):
                        if qty > 0 and not qty in quantity_dict.keys():
                            quantity_dict[str(qty)] = filler
                            
                    # form primary columns
                    input_dict = {"Product Name" : products_list, "Orders" : filler }
                    # update the quantiy list
                    input_dict.update(quantity_dict)
                    # update mixed orders condition
                    order_ids = report_df['amazon-order-id'].to_list()
                    product_names = report_df['product-name'].to_list()
                    if len(order_ids) < len(product_names):
                        input_dict.update({"Mixed" : filler})
                    # add the rest
                    input_dict.update({
                        'Total Qty' : filler,
                        'Rate' : filler,'Amount' : filler
                    })
                    # and fill it with datas.
                    sorted_instance = LabelSorter(pdf_path=label_path)
                    print(sorted_instance)
            else:
                input_dict = {}
            tally_df = pd.DataFrame(input_dict)
            return tally_df
        except Exception as e:
            return pd.DataFrame({"Error" : e})
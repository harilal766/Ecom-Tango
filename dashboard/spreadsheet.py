from datetime import datetime, timedelta
import pandas as pd, os, json
from openpyxl import load_workbook
from styleframe import StyleFrame, Styler
import re


class Spreadsheet:
    def __init__(self, store, df):
        self.df = df
        self.store = store
        
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
            pass
    
    def create_tally_table(self, products_list: list, pivot_df):
        tally_df = None
        filler = [None] * len(products_list)
        print(f'Fillers : {filler}')
        try:
            tally_df = pd.DataFrame({
                'Product Name' : pivot_df['Row Labels'].to_list(),
                'Orders' : filler,
                '1' : filler,'2' : filler,'3' : filler,
                'Mixed' : filler,
                'Total Qty' : filler,
                'Rate' : filler,
                'Amount' : filler
            })
            return tally_df
        except Exception as e:
            pass
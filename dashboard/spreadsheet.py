import pandas as pd

class Spreadsheet:
    def __init__(self, report_type, df):
        self.main_sheet = df
            
    def create_pivot_table(self,index,other_columns):
        pivot_df = None
        try:
            if index and other_columns:
                pivot_df = self.main_sheet.pivot_table(
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
    
    def create_tally_table(self, products_list: list):
        tally_df = None
        filler = [None] * len(products_list)
        print(f'Fillers : {filler}')
        try:
            tally_df = pd.DataFrame({
                'Product Name' : products_list,
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
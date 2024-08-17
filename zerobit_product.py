import pandas as pd

class Product:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def get_product_names(self):
        return self.data['Product Name'].tolist()
    
    
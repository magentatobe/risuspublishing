#!/usr/bin/python3

import collections
import csv
import datetime
import os
import os.path
import random

from risuspubl import create_app
from risuspubl.dbmodels import *


table_names = ['authors_manuscripts', 'authors_books', 'books', 'authors', 'manuscripts', 'editors', 'clients',
               'salespeople', 'sales_records', 'series']

table_to_id_column = {'authors': 'author_id', 'books': 'book_id', 'clients': 'client_id', 'editors': 'editor_id',
                      'manuscripts': 'manuscript_id', 'sales_records': 'sales_record_id',
                      'salespeople': 'salesperson_id', 'series': 'series_id'}

table_to_model_class = {'authors': Author, 'books': Book, 'clients': Client, 'editors': Editor, 'manuscripts': Manuscript,
                      'sales_records': SalesRecord, 'salespeople': Salespeople, 'series': Series}

model_objs = collections.defaultdict(list)

model_ids = collections.defaultdict(list)

data_dir = './data/'


app = create_app()
app.app_context().push()

db = SQLAlchemy(app)


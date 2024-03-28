import pandas as pd
import numpy as np
from functools import reduce

data = pd.read_csv('BL-Flickr-Images-Book.csv')
data.head()

to_drop = ['Edition Statement',
           'Corporate Author',
           'Corporate Contributors',
           'Former owner',
           'Engraver',
           'Contributors',
           'Issuance type',
           'Shelfmarks']

data.drop(to_drop, inplace = True, axis = 1)
data.head()

data.set_index('Identifier', inplace = True)
#Jadi, ketika Anda menulis inplace=True, itu berarti Anda ingin mengubah DataFrame yang asli dengan mengatur indeks baru
data.head()

data.loc[216]

data['Date of Publication'].head(25)

unwanted_characters = ['[', ',', '-']

def clean_dates(item):
    dop= str(item.loc['Date of Publication'])
    
    if dop == 'nan' or dop[0] == '[':
        return np.NaN
    
    for character in unwanted_characters:
        if character in dop:
            character_index = dop.find(character)
            dop = dop[:character_index]
    
    return dop

data['Date of Publication'] = data.apply(clean_dates, axis = 1)

#alternate way of cleaning Date of Publication
#run cell to see output
unwanted_characters = ['[', ',', '-']

def clean_dates(dop):
    dop = str(dop)
    if dop.startswith('[') or dop == 'nan':
        return 'NaN'
    for character in unwanted_characters:
        if character in dop:
            character_index = dop.find(character)
            dop = dop[:character_index]
    return dop

data['Date of Publication'] = data['Date of Publication'].apply(clean_dates)
data.head()

def clean_author_names(author):
    
    author = str(author)
    
    if author == 'nan':
        return 'NaN'
    
    author = author.split(',')

    if len(author) == 1:
        name = filter(lambda x: x.isalpha(), author[0])
        return reduce(lambda x, y: x + y, name)
    
    last_name, first_name = author[0], author[1]

    first_name = first_name[:first_name.find('-')] if '-' in first_name else first_name
    
    if first_name.endswith(('.', '.|')):
        parts = first_name.split('.')
        
        if len(parts) > 1:
            first_occurence = first_name.find('.')
            final_occurence = first_name.find('.', first_occurence + 1)
            first_name = first_name[:final_occurence]
        else:
            first_name = first_name[:first_name.find('.')]
    
    last_name = last_name.capitalize()
    
    return f'{first_name} {last_name}'


data['Author'] = data['Author'].apply(clean_author_names)

data.head()

def clean_title(title):
    
    if title == 'nan':
        return 'NaN'
    
    if title[0] == '[':
        title = title[1: title.find(']')]
        
    if 'by' in title:
        title = title[:title.find('by')]
    elif 'By' in title:
        title = title[:title.find('By')]
        
    if '[' in title:
        title = title[:title.find('[')]

    title = title[:-2]
        
    title = list(map(str.capitalize, title.split()))
    return ' '.join(title)
    
data['Title'] = data['Title'].apply(clean_title)
data.head()

#4157862 and 4159587
data.loc[4159587]

data.head()


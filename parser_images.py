import numpy as np
import pandas as pd
from pandas.core.indexing import check_bool_indexer
import requests
import numpy as np
import json
import Levenshtein

df = pd.read_csv('users_raw.csv', encoding='utf-16')

# ====Getting users that have an icon====
df = df[df["Изображение пользователя"].str.contains("pluginfile.php")]
# ====Getting only currently studying students====
d = json.load(open('data.json', 'r', encoding='utf-8'))

for key in d:
    classes_df = pd.read_csv(d[key]['file_path'], encoding='utf-16')
    
    # del classes_df['Группа']
    # del classes_df['Дата рождения']
    classes_df = classes_df.rename(columns={'ФИО': 'Фамилия / Имя'})
    
    images = []
    for i in classes_df.itertuples():
        m = -1
        name = None
        url = None
        for j in df.itertuples():
            jaro = Levenshtein.jaro(i._1, j._2)
            if jaro > m:
                m = jaro
                ind = j.Index
                url = j._1
                name = j._2
        url = url[:url.index(r'%2Fclean')]
        images.append(url)

    classes_df['Изображение пользователя'] = images
    classes_df.to_csv('csv_classes/' + key + '.csv', index=False, encoding='utf-16')

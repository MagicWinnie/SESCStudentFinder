# Find a person studying at SESC of NSU
## Usage  
1. Install dependencies:  
   * `pip install -r requirements.txt`
   * Install `geckodriver`
2. Create a `website_login_data.json` file containing your login data with the following structure:
    ```json
    {
        "login": "your login",
        "password": "your password"
    }
    ```
3. `python parser_table.py`  
   The script parses the list of students from sesc.nsu.ru/edu/moodle.  
   It generates a `users_raw.csv` file.  
4. Create `.csv` files for each grade and put them into `csv_classes` folder next in the root of the project.  
   It must have the following columns/column header names:  
   `Фамилия / Имя,Группа,Дата рождения` 
5. Create a `data.json` file containing with the following structure:
    ```json
    {
        "9-1": {
            "file_path": "path/to/csv/with/students",
            "tutor": "Иванов Иван Иванович"
        },
        // and so on
    }
    ```
6. `python parser_images.py`  
   It adds to existing `.csv` files a column with URLs for users' icons.
7. `python scraping_images.py where/to/save/images`  
   Downloads users' icons.  
8. `python extract_features.py`  
   It creates a `dataset_faces.dat` file with face encodings.
9.  `python find_person.py`  
   An GUI application to find people.
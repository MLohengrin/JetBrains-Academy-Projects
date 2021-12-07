# Convoy Shipping Company

import json
import pandas as pd
import csv
import re
import sqlite3
from lxml import etree


def input_xlsx(file_name):
    df = pd.read_excel(fr'{file_name}.xlsx', sheet_name='Vehicles', dtype=str)
    return df


def output_csv(df, file_name):
    df.to_csv(fr'{file_name}.csv', index=None)


def get_file_name():
    print('Input file name')
    file_name = input()
    return file_name


def count_entries(df):
    entries = df.shape[0]
    return entries


def xlsx_to_csv(file_name):
    file_name = file_name.removesuffix('.xlsx')
    df = input_xlsx(file_name)
    entries = count_entries(df)
    output_csv(df, file_name)
    print(f'{entries} {"line was" if entries == 1 else "lines were"} imported to {file_name}.csv')
    return file_name.removesuffix('.xlsx') + '.csv'


def get_csv(file_name):
    if file_name.endswith('.xlsx'):
        file_name = xlsx_to_csv(file_name)
    elif not file_name.endswith('.csv'):
        exit()
    csv_data = []
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for line in reader:
            csv_data.append(line)
    return csv_data


def cell_to_digit(cell):
    digits = re.findall(r'\d+', cell)
    return digits[0]


def fix_data(csv_data):
    fixed_data = []
    row = 0
    fixed_cells = 0
    for line in csv_data:
        if row == 0:
            fixed_data.append(line)
        else:
            new_row = []
            for cell in line:
                if cell.isdigit():
                    new_row.append(cell)
                else:
                    new_row.append(cell_to_digit(cell))
                    fixed_cells += 1
            fixed_data.append(new_row)
        row += 1
    return fixed_data, fixed_cells


def write_data(csv_data, out_name):
    with open(out_name, 'w', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=',', lineterminator="\n")
        for row in csv_data:
            file_writer.writerow(row)


def output_message(out_name, fixed_cells):
    print(f'{fixed_cells} {"cell was" if fixed_cells == 1 else "cells were"} corrected in {out_name}')


def get_out_name(file_name):
    file_name_dot_index = file_name.rfind('.')
    out_name = file_name[:file_name_dot_index] + '[CHECKED].csv'
    return out_name


def check_csv(file_name):
    if not file_name.endswith('[CHECKED].csv'):
        csv_data = get_csv(file_name)
        fixed_data, fixed_cells = fix_data(csv_data)
        out_name = get_out_name(file_name)
        write_data(fixed_data, out_name)
        output_message(out_name, fixed_cells)
        file_name = out_name
    csv_data = []
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for line in reader:
            csv_data.append(line)
    db_name = file_name[:file_name.rfind('[')] + '.s3db'
    return csv_data, db_name


def create_and_connect(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def calculate_score(row):
    engine_capacity = int(row[1])
    fuel_consumption = int(row[2])
    maximum_load = int(row[3])
    fuel_consumed = (450 / (100 / fuel_consumption))
    pitstops = int(fuel_consumed / engine_capacity)
    score = 1
    if pitstops == 0:
        score += 2
    elif pitstops == 1:
        score += 1
    if fuel_consumed <= 230:
        score += 1
    if maximum_load >= 20:
        score += 2
    return score


def populate_db(my_db, csv_checked):
    cursor = my_db.cursor()
    cursor.execute('CREATE TABLE convoy('
                   'vehicle_id INT PRIMARY KEY,'
                   'engine_capacity INT NOT NULL,'
                   'fuel_consumption INT NOT NULL,'
                   'maximum_load INT NOT NULL,'
                   'score INT NOT NULL);')
    line_count = 0
    for row in csv_checked:
        if line_count == 0:
            line_count += 1
            continue
        score = calculate_score(row)
        cursor.execute(f'INSERT INTO convoy VALUES({row[0]}, {row[1]}, {row[2]}, {row[3]}, {score});')
        line_count += 1
    my_db.commit()
    my_db.close()
    return line_count - 1


def populated_message(db_name, n_records):
    print(f'{n_records} {"record was" if n_records == 1 else "records were"} inserted into {db_name}')


def check_db_ready(file_name):
    if not file_name.endswith('s3db'):
        csv_checked, db_name = check_csv(file_name)
        my_db = create_and_connect(db_name)
        n_records = populate_db(my_db, csv_checked)
        populated_message(db_name, n_records)
    else:
        db_name = file_name
    return db_name


def db_to_dict(db_name, score_threshold):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    result = cursor.execute(f'SELECT * FROM convoy WHERE score {score_threshold}')
    all_rows = result.fetchall()
    db_dict = {'convoy': []}
    for row in all_rows:
        new_row = {
            "vehicle_id": row[0],
            "engine_capacity": row[1],
            "fuel_consumption": row[2],
            "maximum_load": row[3]
        }
        db_dict['convoy'].append(new_row)
    conn.close()
    return db_dict, len(db_dict['convoy'])


def generate_json(db_name):
    db_dict, n_vehicles = db_to_dict(db_name, '> 3')
    json_name = db_name[:db_name.rfind('.')] + '.json'
    with open(json_name, 'w') as json_file:
        json.dump(db_dict, json_file)
    print(f'{n_vehicles} {"vehicle was" if n_vehicles == 1 else "vehicles were"} saved into {json_name}')
    return json_name


def generate_xml(db_name):
    db_dict, n_vehicles = db_to_dict(db_name, '<= 3')
    xml_string = "<convoy>\n"
    for vehicle in db_dict['convoy']:
        xml_string += '<vehicle>\n'
        for field, value in vehicle.items():
            xml_string += f'<{field}>{value}</{field}>\n'
        xml_string += '</vehicle>\n'
    xml_string += "</convoy>"
    root = etree.fromstring(xml_string)
    tree = etree.ElementTree(root)
    xml_name = db_name[:db_name.rfind('.')] + '.xml'
    with open(xml_name, 'w') as xml_file:
        tree.write(xml_name)
    print(f'{n_vehicles} {"vehicle was" if n_vehicles == 1 else "vehicles were"} saved into {xml_name}')
    return xml_name


def main():
    file_name = get_file_name()
    db_name = check_db_ready(file_name)
    generate_json(db_name)
    generate_xml(db_name)


main()

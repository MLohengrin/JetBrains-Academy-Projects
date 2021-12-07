# Easy Rider Bus Company

import json
import re
from collections import defaultdict


def check_bus_id(value):
    if not value:
        return 1
    if type(value) != int:
        return 1
    return 0


def check_stop_id(value):
    if not value:
        return 1
    if type(value) != int:
        return 1
    return 0


def check_stop_name(value):
    if not value:
        return 1
    if type(value) != str:
        return 1
    template = r'[A-Z].* (Road|Avenue|Boulevard|Street)$'
    if not re.match(template, value):
        return 1
    return 0


def check_next_stop(value):
    if not value and value != 0:
        return 1
    if type(value) != int:
        return 1
    return 0


def check_stop_type(value):
    if type(value) != str:
        return 1
    if len(value) > 1 or value not in 'SOF':
        return 1
    return 0


def check_a_time(value):
    if not value:
        return 1
    if type(value) != str:
        return 1
    template = r'([0-1][0-9]|2[0-3]):[0-5][0-9]$'
    if not re.match(template, value):
        return 1
    return 0


def check_data(input_dict):
    error_dict = {'bus_id': 0,
                  'stop_id': 0,
                  'stop_name': 0,
                  'next_stop': 0,
                  'stop_type': 0,
                  'a_time': 0}
    for stop in input_dict:
        # error_dict['bus_id'] += check_bus_id(stop['bus_id'])
        # error_dict['stop_id'] += check_stop_id(stop['stop_id'])
        error_dict['stop_name'] += check_stop_name(stop['stop_name'])
        # error_dict['next_stop'] += check_next_stop(stop['next_stop'])
        error_dict['stop_type'] += check_stop_type(stop['stop_type'])
        error_dict['a_time'] += check_a_time(stop['a_time'])
    return error_dict


def output_errors(errors):
    tot_err = 0
    for err_type in errors.values():
        tot_err += err_type
    # if tot_err:
    print(f'Format validation: {tot_err} errors')
    # if errors["bus_id"]:
    # print(f'bus_id: {errors["bus_id"]}')
    # if errors["stop_id"]:
    # print(f'stop_id: {errors["stop_id"]}')
    # if errors["stop_name"]:
    print(f'stop_name: {errors["stop_name"]}')
    # if errors["next_stop"]:
    # print(f'next_stop: {errors["next_stop"]}')
    # if errors["stop_type"]:
    print(f'stop_type: {errors["stop_type"]}')
    # if errors["a_time"]:
    print(f'a_time: {errors["a_time"]}')


def output_bus_lines(input_dict):
    lines_dict = defaultdict(int)
    for stop in input_dict:
        if not check_bus_id(stop['bus_id']):
            lines_dict[stop['bus_id']] += 1
    print('Line names and number of stops:')
    for k, v in lines_dict.items():
        print(f'bus_id: {k}, stops: {v}')


def get_input():
    input_json = input()
    input_dict = json.loads(input_json)
    return input_dict


def main():
    input_dict = get_input()
    # errors = check_data(input_dict)
    # output_errors(errors)
    output_bus_lines(input_dict)


main()

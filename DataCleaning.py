import re


def clean_data_names(data):
    data = str(data)
    data = ''.join(i for i in data if i.isalnum() or i == ' ')
    data = data.lower().strip()
    data = re.sub(' +', ' ', data)
    return '\'' + data + '\''


def clean_data_text(data):
    data = str(data)
    if 'http' in data:
        data = data.split('http')[0]
    if '@' in data:
        data_arr = data.split()
        data = ''.join(i + ' ' for i in data_arr if '@' not in i)
    data = ''.join(i for i in data if i.isalnum() or i == ' ')
    data = data.lower().strip()
    data = re.sub(' +', ' ', data)
    return '\'' + data + '\''


def clean_data_other(data):
    return '\'' + str(data) + '\''


def clean_data_loc(data, states, state_names):
    data = str(data)
    data = ''.join(i for i in data if i.isalnum() or i == ' ')
    data = data.lower().strip()
    data = re.sub(' +', ' ', data)

    if any(' ' + states[i] in data or states[i] + ' ' in data or state_names[i] in data
           for i in range(len(states))) or 'united states' in data or 'usa' in data:

        for i in range(len(state_names)):
            data = data.replace(state_names[i], states[i]).strip()

        if data == 'united states' or data == 'usa':
            return '\'na, na, usa\''
        if data[-3:] == 'usa':
            data = data[:-3].strip()
        elif data[-13:] == 'united states':
            data = data[:-13].strip()

        if data[-3:].strip() in states:
            if data[:-2]:
                data = data[:-3] + ',' + data[-3:] if ' ' in data[-3:] else ', na'
            else:
                data = 'na, ' + data
        else:
            data = data + ', na'
    else:
        data = 'NULL'

    return '\'' + data + ', usa\'' if data != 'NULL' else data

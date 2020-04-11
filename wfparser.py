from bs4 import BeautifulSoup
import requests
import os
import pathlib
import json
import hashlib


def parse_item(item):
    if 'mark' in item['class']:
        type = 'mark'
    elif 'stripe' in item['class']:
        type = 'stripe'
    elif 'badge' in item['class']:
        type = 'badge'
    elif 'console' in item['class']:
        type = 'console'
    else:
        return {}

    image_path = item.find('div', class_='picture').img['src']
    return {
        'id': pathlib.Path(image_path).stem,
        'type': type,
        'name': item.find('div', class_='name').a.string.strip(),
        'desc': item.find('div', class_='description').string.strip(),
        'image': image_path
    }


def get_name_from_path(path):
    return pathlib.Path(path).name


def download_image(to_dir, image_path, base_url):
    file_name = get_name_from_path(image_path)
    file_path = '/'.join([to_dir, file_name])
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)

    image_data = requests.get(base_url + image_path)
    if len(image_data.content) > 0:
        f = open(file_path, 'wb')
        f.write(image_data.content)
        f.close()
    else:
        return False

    return file_path


def get_existing_hash(out_dir):
    try:
        with open(out_dir + '/hash') as f:
            return f.read()
    except IOError:
        return False


def need_parse(data, out_dir):
    currentHash = hashlib.md5(data.encode()).hexdigest()
    oldHash = get_existing_hash(out_dir)
    if oldHash == currentHash:
        return False
    else:
        with open(out_dir + '/hash', 'w') as write_file:
            write_file.write(currentHash)
            write_file.close()
        return True


def run(out_dir, base_url, endpoint):
    page_url = base_url + endpoint
    page = requests.get(page_url)

    parsed_achievements = {
        'mark': [],
        'stripe': [],
        'badge': [],
        'console': []
    }

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")

        achievements = soup.findAll('div', class_='achievement')
        achievements = list(filter(lambda item: 1 if str(item['id']).isdigit() == False else 0, achievements))

        for item in achievements:
            parsed_item = parse_item(item)
            if len(parsed_item) > 0:
                parsed_achievements[parsed_item['type']].append(parsed_item)

        if need_parse(json.dumps(parsed_achievements), out_dir):

            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            for category in parsed_achievements:
                for i in range(len(parsed_achievements[category])):
                    image_path = '/'
                    if image_path == False:
                        print('ERROR', parsed_achievements[category][i]['name'])
                        del parsed_achievements[category][i]
                    else:
                        parsed_achievements[category][i]['image'] = image_path

            with open('achievements.json', 'w') as write_file:
                json.dump(parsed_achievements, write_file)
        else:
            return None

    return parsed_achievements

import os
import json

from resources.resource import RESOURCE_DIR


def get_live2d_texture_path(model_json_path):
    with open(model_json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    textures = json_data.get('FileReferences', {}).get('Textures')[0]
    return os.path.join(RESOURCE_DIR, textures)
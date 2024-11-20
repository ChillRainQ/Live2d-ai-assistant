import os

PERSONALITY_DIR_NAME = 'personalities'
CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PERSONALITY_DIR_PATH = os.path.join(CURRENT_DIR_PATH, PERSONALITY_DIR_NAME)


def load_personality(choice: str) -> str:
    """
    加载人设
    """
    return _read_content(os.path.join(PERSONALITY_DIR_PATH, choice + '.txt'))


def get_personalities_list() -> list:
    results = []
    for _, _, files in os.walk(PERSONALITY_DIR_PATH):
        for file in files:
            file = file[:-4]
            results.append(file)
    return results



def _read_content(file_name: str) -> str:

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f'{file_name} not found')

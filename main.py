
from application import Application
from config.application_config import ApplicationConfig
from core.gobal_components import i18n

config = ApplicationConfig()
config.setup()

if __name__ == '__main__':

    # print("application init....")
    # app = Application(config)
    # print("load config....")
    # app.load_config()
    # print("setup app....")
    # app.setup()
    # print("run app....")
    # app.start()

    # main.main.init
    print(f"{i18n.get_str('main.main.init')}")
    app = Application(config)
    # main.main.loadConfig
    print(f"{i18n.get_str('main.main.loadConfig')}")
    app.load_config()
    # main.main.setupApp
    print(f"{i18n.get_str('main.main.setupApp')}")
    app.setup()
    # main.main.runApp
    print(f"{i18n.get_str('main.main.runApp')}")
    app.start()
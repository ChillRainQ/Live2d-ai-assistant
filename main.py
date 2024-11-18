
from application import Application
from config.application_config import ApplicationConfig

config = ApplicationConfig()

if __name__ == '__main__':
    print("application init....")
    app = Application(config)
    print("load config....")
    app.load_config()
    print("setup app....")
    app.setup()
    print("run app....")
    app.start()
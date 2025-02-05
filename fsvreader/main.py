from fsvreader import config, server

settings = config.Settings()

app = server.create_server(settings=settings)

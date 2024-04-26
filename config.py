from configparser import ConfigParser
import boto3


def load_config(filename="database.ini", section="aws-iam"):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config


def load_config_iam(filename="database.ini", section="aws-database-1"):
    preconfig_user = load_config(filename="database.ini", section="aws-iam")
    # This is dirty but these are not secrets. I had to put these here because the parser changes to lowercase for some reason.
    preconfig_token = {
        "DBHostname": "database-1.c3eweo0wsv9b.eu-north-1.rds.amazonaws.com",
        "Port": "5432",
        "DBUsername": "db_user",
        "Region": "eu-north-1",
    }
    client = boto3.client("rds", **preconfig_user)
    token = client.generate_db_auth_token(**preconfig_token)
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
        config["password"] = token
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config


if __name__ == "__main__":
    config = load_config()
    print(config)

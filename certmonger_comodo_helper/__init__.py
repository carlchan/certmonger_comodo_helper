try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from certmonger_comodo_helper import *


def main():
    # Set a default as it may not exist.
    config = configparser.ConfigParser({'api_url': 'https://hard.cert-manager.com/ws/EPKIManagerSSL?wsdl',
                                        'ca_poll_wait': 60,
                                        'client_cert_auth': 'false',
                                        'password': None})

    config.read('/etc/certmonger/comodo.ini')
    kwargs = dict(config.items('default'))
    # A little funny, but I want the value to come through as a bool not str.
    kwargs['client_cert_auth'] = config.getboolean('default', 'client_cert_auth')

    crt = ComodoTLSService(**kwargs)

    env = get_environment()

    if env['CERTMONGER_OPERATION'] == 'SUBMIT':
        crt.submit(cert_type_name=config.get('default', 'cert_type_name'),
                   revoke_password=config.get('default', 'revoke_password'),
                   term=config.get('default', 'term'))
    elif env['CERTMONGER_OPERATION'] == 'POLL':
        crt.poll()
    else:
        sys.exit(6)
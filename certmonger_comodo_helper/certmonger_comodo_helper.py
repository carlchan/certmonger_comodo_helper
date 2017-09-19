#!/usr/bin/env python
import os
import suds.client
import sys


def get_environment():
    """
    This method gathers the environment variables and returns only the
    environment variables matching 'CERTMONGER.*'

    :return: A dictionary containing all CERTMONGER env keys and values.
    :rtype: dict
    """
    sanitized = {}

    for key, value in os.environ.items():
        if 'CERTMONGER' in key:
            sanitized[key] = value

    return sanitized


class ComodoCA(object):
    """
    Top level class for the Comodo CA. Only very generic 'things' go here.
    """

    format_type = {'X509 PEM Bundle': 0,
                   'X509 PEM Certificate only': 1,
                   'X509 PEM Intermediate certificate only': 2,
                   'PKCS#7 PEM Bundle': 3,
                   'PKCS#7 DER Bundle': 4}

    formats = {'AOL': 1,
               'Apache/ModSSL': 2,
               'Apache-SSL': 3,
               'C2Net Stronghold': 4,
               }

    status_code = {1: 'Certificate available',
                   2: 'Certificates Attached',
                   0: 'Certificate being processed by Comodo',
                   -10: 'The CSR cannot be decoded!',
                   -11: 'The CSR uses an unsupported algorithm!',
                   -12: 'The CSR has an invalid signature!',
                   -13: 'The CSR uses an unsupported key size!',
                   -14: 'An unknown error occurred!',
                   -16: 'Permission denied!',
                   -20: 'The certificate request has been rejected!',
                   -21: 'The certificate has been revoked!',
                   -22: 'Still awaiting payment!',
                   -31: 'The email is not a valid email.',
                   -32: 'The two phrase should be the same!',
                   -33: 'The Comodo certificate type is invalid!',
                   -34: 'The secret key is invalid!',
                   -35: 'The server type is invalid!',
                   -36: 'The term is invalid for customer type!',
                   -40: 'Invalid ID',
                   -100: 'Invalid authentication data for customer',
                   -101: 'Invalid authentication data for customer Organization',
                   -110: 'Domain is not allowed for customer',
                   -111: 'Domain is not allowed for customer Organization',
                   -120: 'Customer configuration is not allowed the requested action',
                   }


class ComodoTLSService(ComodoCA):
    """

    """

    def __init__(self, customer_login_uri, org_id, password, secret_key, login,
                 api_url='https://hard.cert-manager.com/ws/EPKIManagerSSL?wsdl'):
        """
        :param string api_url: The full URL for the API server
        :param string customer_login_uri: The URI for the customer login (if your login to the Comodo GUI is at
                https://hard.cert-manager.com/customer/foo/, your login URI is 'foo').
        :param string org_id: The organization ID
        :param string password: The API user's password
        :param string secret_key: The API user's secret key
        :param string login: The API user
        """
        self.api_url = api_url
        self.customer_login_uri = customer_login_uri
        self.org_id = org_id
        self.password = password
        self.secret_key = secret_key
        self.login = login
        self.client = suds.client.Client(self.api_url)
        self.auth = self.client.factory.create('authData')
        self.auth.login = self.login
        self.auth.password = self.password
        self.auth.customerLoginUri = self.customer_login_uri
        self.env = get_environment()

    def get_cert_types(self):
        """
        Collect the certificate types that are available to the customer.

        :return: A list of dictionaries of certificate types
        :rtype: list
        """
        result = self.client.service.getCustomerCertTypes(authData=self.auth)

        # Very basic error checking
        if result.statusCode != 0:
            print(ComodoCA.status_code[result.statusCode])
            sys.exit(3)
        else:
            return result.types

    def poll(self):
        """
        Poll for certificate availability after submission.
        :return:
        """
        result = self.client.service.collect(authData=self.auth, id=self.env['CERTMONGER_CA_COOKIE'],
                                             formatType=ComodoCA.format_type['X509 PEM Certificate only'])

        if result['statusCode'] == 2:
            print(result['SSL']['certificate'])
            sys.exit(0)
        elif result['statusCode'] == 0:
            print(self.env['CERTMONGER_CA_COOKIE'])
            sys.exit(1)
        else:
            print(ComodoCA.status_code[result.statusCode])
            sys.exit(3)

        # Should never be reached
        return None

    def submit(self, cert_type_name, revoke_password, term):
        """
        Submit a certificate request to Comodo.

        :param string cert_type_name: The full cert type name (Example: 'PlatinumSSL Certificate')
        :param string revoke_password: A password for certificate revocation
        :param int term: The length, in years, for the certificate to be issued
        :return: A string indicating the certificate ID to be collected.
        :rtype: string
        """
        cert_types = self.get_cert_types()

        for type in cert_types:
            if type.name == cert_type_name:
                cert_type = type

        # serverType is hard coded to 2 as this is being passed back to certmonger that can transform the PEM to
        # whatever is required.
        result = self.client.service.enroll(authData=self.auth, orgId=self.org_id, secretKey=self.secret_key,
                                            csr=self.env['CERTMONGER_CSR'], phrase=revoke_password,
                                            subjAltNames=self.env.get('CERTMONGER_REQ_HOSTNAME', ''),
                                            certType=cert_type, numberServers=1,
                                            serverType=ComodoCA.formats['Apache/ModSSL'], term=term, comments='')

        if result > 0:
            print(result)
            sys.exit(1)
        else:
            print(ComodoCA.status_code[result.statusCode])
            sys.exit(2)

        # Should never be reached
        return None
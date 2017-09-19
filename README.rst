The certmonger_comodo_helper is a helper for certmonger that submits and gathers certificates from the Comodo API. 
It is written in python and requires the suds python library, it should be compatible with both python 3 and 2.

The comodo_client.py files needs to be placed into /usr/libexec/certmonger (on RHEL like systems) and a CA 
configuration must be added to /var/lib/certmonger/cas/comodo with the following contents:
    
    id=comodo
    ca_is_default=0
    ca_type=EXTERNAL
    ca_external_helper=/usr/libexec/certmonger/comodo_client.py
    
Further the following config must be in place in /etc/certmonger/comodo.ini, you will need to either generate these 
resources yourself from the Comodo UI or speak with Comodo:

    api_url= # Example: https://hard.cert-manager.com/ws/EPKIManagerSSL?wsdl>
    cert_type_name= # The prefered certificate type, example: PlatinumSSL Certificate>
    customer_login_uri= # The login uri for the customer, if you login to the Comodo Certificate Manager (CCM) 
                          at https://hard.cert-manager.com/customer/foo, your URI is foo>
    login= # The login name to use
    org_id= # Your organization ID, can be found in CCM
    password= # The password for the user
    revoke_password= # A certificate revocation password (this is required though never used)
    secret_key= # You API secret key
    term= # The term you wish for your certificate to be valid in years

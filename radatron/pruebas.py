#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
Created on 28 ago. 2019
#!/usr/bin/python

@author: joseb
Notas:
#!/usr/bin/python
    Es una shebang line. Tiene una función en Unix o Linux. En Windows no hace nada.
    Also called a hashbang, hashpling, pound bang, or crunchbang)
    refers to the characters "#!" when they are the first two characters in an interpreter directive as the first line of a text file.
    In a Unix-like operating system, the program loader takes the presence of these two characters as an indication that the file is a script,
    and tries to execute that script using the interpreter specified by the rest of the first line in the file.
    Diferencia entre #!/usr/bin/python y #!/usr/bin/env:
        #!/usr/bin/python is hardcoded to always run /usr/bin/python, while #!/usr/bin/env python will run whichever python would be default in your current environment
        (it will take in account for example $PATH, you can check which python interpreter will be used with which python). 
Codigos de caracteres:
    # -*- coding: UTF8 -*-
    # -*- coding: cp1252 -*-
'''

import time, datetime
import numpy as np

#Librerias para mostrar las imagenes:
#Ver https://likegeeks.com/python-image-processing/
#Ver https://techtutorialsx.com/2017/04/30/python-opencv-reading-and-displaying-an-image/
#Ver https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot
#import matplotlib.pyplot as plt
from PIL import Image
#import cv2 # pip install opencv-python

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#Formatos de fecha y hora
if False:
    ahora = datetime.datetime.now() #<class 'datetime.datetime'>
    print('ahora datetime     ->', ahora, type(ahora)) #<class 'str'>
    ahoraFormateado = str(datetime.datetime.now()).replace(' ', '_').replace(':', 'h')[:16]
    print('ahora formateado   ->', ahoraFormateado, type(ahoraFormateado)) #<class 'str'>
    hoyDate = datetime.date.today()
    hoyTexto = str(datetime.date.today()).replace('-', '_')
    fecha = hoyDate.strftime("%Y_%B_%A")
    print('hoy date           ->', hoyDate, type(hoyDate)) #<class 'datetime.date'>
    print('hoy text           ->', hoyTexto, type(hoyTexto)) #<class 'str'>
    hoyDateFormateado = hoyDate.strftime("%Y_%B_%A")
    print('fecha              ->', hoyDateFormateado, type(hoyDateFormateado)) #<class 'str'>
    dateTimeFormateado = time.asctime(time.localtime(time.time())).replace(' ', '_').replace(':', ':')
    print('dateTimeFormateado ->', dateTimeFormateado, type(dateTimeFormateado)) #<class 'str'>
    quit()
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#Pruebas de conexion a Internet básica, sin login
if False:
    miUrl = 'https://api.github.com'
    try:
        response1 = requests.get(miUrl)
        response1.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('prueba1:', response1)
        print('prueba1 headers:', type(response1.headers), dir(response1.headers))
        #<class 'requests.structures.CaseInsensitiveDict'> ['_MutableMapping__marker', '__abstractmethods__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', '_store', 'clear', 'copy', 'get', 'items', 'keys', 'lower_items', 'pop', 'popitem', 'setdefault', 'update', 'values']
        print('             ->:', response1.headers)
        #{'Date': 'Fri, 30 Aug 2019 16:29:47 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Server': 'GitHub.com', 'Status': '200 OK', 'X-RateLimit-Limit': '60', 'X-RateLimit-Remaining': '59', 'X-RateLimit-Reset': '1567186187', 'Cache-Control': 'public, max-age=60, s-maxage=60', 'Vary': 'Accept, Accept-Encoding', 'ETag': 'W/"7dc470913f1fe9bb6c7355b50a0737bc"', 'X-GitHub-Media-Type': 'github.v3; format=json', 'Access-Control-Expose-Headers': 'ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type', 'Access-Control-Allow-Origin': '*', 'Strict-Transport-Security': 'max-age=31536000; includeSubdomains; preload', 'X-Frame-Options': 'deny', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block', 'Referrer-Policy': 'origin-when-cross-origin, strict-origin-when-cross-origin', 'Content-Security-Policy': "default-src 'none'", 'Content-Encoding': 'gzip', 'X-GitHub-Request-Id': 'AEA8:2100B:48488E4:581733B:5D694EFB'}
        print('prueba1 content:', type(response1.content), dir(response1.content))
        #<class 'bytes'> ['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'center', 'count', 'decode', 'endswith', 'expandtabs', 'find', 'fromhex', 'hex', 'index', 'isalnum', 'isalpha', 'isascii', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
        print('             ->:', response1.content)
        #b'{"current_user_url":"https://api.github.com/user","current_user_authorizations_html_url":"https://github.com/settings/connections/applications{/client_id}","authorizations_url":"https://api.github.com/authorizations","code_search_url":"https://api.github.com/search/code?q={query}{&page,per_page,sort,order}","commit_search_url":"https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}","emails_url":"https://api.github.com/user/emails","emojis_url":"https://api.github.com/emojis","events_url":"https://api.github.com/events","feeds_url":"https://api.github.com/feeds","followers_url":"https://api.github.com/user/followers","following_url":"https://api.github.com/user/following{/target}","gists_url":"https://api.github.com/gists{/gist_id}","hub_url":"https://api.github.com/hub","issue_search_url":"https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}","issues_url":"https://api.github.com/issues","keys_url":"https://api.github.com/user/keys","notifications_url":"https://api.github.com/notifications","organization_repositories_url":"https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}","organization_url":"https://api.github.com/orgs/{org}","public_gists_url":"https://api.github.com/gists/public","rate_limit_url":"https://api.github.com/rate_limit","repository_url":"https://api.github.com/repos/{owner}/{repo}","repository_search_url":"https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}","current_user_repositories_url":"https://api.github.com/user/repos{?type,page,per_page,sort}","starred_url":"https://api.github.com/user/starred{/owner}{/repo}","starred_gists_url":"https://api.github.com/gists/starred","team_url":"https://api.github.com/teams","user_url":"https://api.github.com/users/{user}","user_organizations_url":"https://api.github.com/user/orgs","user_repositories_url":"https://api.github.com/users/{user}/repos{?type,page,per_page,sort}","user_search_url":"https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"}'
        print('prueba1 text:   ', type(response1.text), dir(response1.text))
        #<class 'str'> ['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
        print('          ->:   ', response1.text)
        #{"current_user_url":"https://api.github.com/user","current_user_authorizations_html_url":"https://github.com/settings/connections/applications{/client_id}","authorizations_url":"https://api.github.com/authorizations","code_search_url":"https://api.github.com/search/code?q={query}{&page,per_page,sort,order}","commit_search_url":"https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}","emails_url":"https://api.github.com/user/emails","emojis_url":"https://api.github.com/emojis","events_url":"https://api.github.com/events","feeds_url":"https://api.github.com/feeds","followers_url":"https://api.github.com/user/followers","following_url":"https://api.github.com/user/following{/target}","gists_url":"https://api.github.com/gists{/gist_id}","hub_url":"https://api.github.com/hub","issue_search_url":"https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}","issues_url":"https://api.github.com/issues","keys_url":"https://api.github.com/user/keys","notifications_url":"https://api.github.com/notifications","organization_repositories_url":"https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}","organization_url":"https://api.github.com/orgs/{org}","public_gists_url":"https://api.github.com/gists/public","rate_limit_url":"https://api.github.com/rate_limit","repository_url":"https://api.github.com/repos/{owner}/{repo}","repository_search_url":"https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}","current_user_repositories_url":"https://api.github.com/user/repos{?type,page,per_page,sort}","starred_url":"https://api.github.com/user/starred{/owner}{/repo}","starred_gists_url":"https://api.github.com/gists/starred","team_url":"https://api.github.com/teams","user_url":"https://api.github.com/users/{user}","user_organizations_url":"https://api.github.com/user/orgs","user_repositories_url":"https://api.github.com/users/{user}/repos{?type,page,per_page,sort}","user_search_url":"https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"}
        print('prueba1 json:   ', type(response1.json), dir(response1.json))
        #<class 'method'> ['__call__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__func__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
        print('          ->:   ', response1.json)
        #<bound method Response.json of <Response [200]>>

    if response1.status_code != 200:
        print('\nError', response1.status_code, 'accediendo:', miUrl)
        #Ver https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

    input('Pulsa un tecla 1')
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#Pruebas de conexion a Internet con login opcion 1 -> conexión puntual, sin crear sesión
if False:
    mi_usuario = 'jbengoam@gmail.com'
    print(f'Para el siguiente requests se solicita contraseña de github.com para el usuario {mi_usuario}')
    response2 = requests.get('https://api.github.com/user', auth=(mi_usuario, getpass()))

    print('prueba2:', response2)
    #print('prueba2 headers:', type(response2.headers), dir(response2.headers))

    print('prueba2 headers:', response2.headers)
    #sin login {'Date': 'Fri, 30 Aug 2019 16:29:47 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Server': 'GitHub.com', 'Status': '200 OK', 'X-RateLimit-Limit': '60', 'X-RateLimit-Remaining': '59', 'X-RateLimit-Reset': '1567186187', 'Cache-Control': 'public, max-age=60, s-maxage=60', 'Vary': 'Accept, Accept-Encoding', 'ETag': 'W/"7dc470913f1fe9bb6c7355b50a0737bc"', 'X-GitHub-Media-Type': 'github.v3; format=json', 'Access-Control-Expose-Headers': 'ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type', 'Access-Control-Allow-Origin': '*', 'Strict-Transport-Security': 'max-age=31536000; includeSubdomains; preload', 'X-Frame-Options': 'deny', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block', 'Referrer-Policy': 'origin-when-cross-origin, strict-origin-when-cross-origin', 'Content-Security-Policy': "default-src 'none'", 'Content-Encoding': 'gzip', 'X-GitHub-Request-Id': 'AEA8:2100B:48488E4:581733B:5D694EFB'}
    #con login {'Date': 'Fri, 30 Aug 2019 16:35:40 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Server': 'GitHub.com', 'Status': '200 OK', 'X-RateLimit-Limit': '5000', 'X-RateLimit-Remaining': '4999', 'X-RateLimit-Reset': '1567186540', 'Cache-Control': 'private, max-age=60, s-maxage=60', 'Vary': 'Accept, Authorization, Cookie, X-GitHub-OTP, Accept-Encoding', 'ETag': 'W/"16b7f66ebba03956efcf2ca32d684a3c"', 'Last-Modified': 'Fri, 30 Aug 2019 16:09:38 GMT', 'X-GitHub-Media-Type': 'github.v3; format=json', 'Access-Control-Expose-Headers': 'ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type', 'Access-Control-Allow-Origin': '*', 'Strict-Transport-Security': 'max-age=31536000; includeSubdomains; preload', 'X-Frame-Options': 'deny', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block', 'Referrer-Policy': 'origin-when-cross-origin, strict-origin-when-cross-origin', 'Content-Security-Policy': "default-src 'none'", 'Content-Encoding': 'gzip', 'X-GitHub-Request-Id': 'AEE0:3BE2E:48E3E70:58C6F76:5D69505C'}

    print('prueba2 content:', response2.content)
    #sin login b'{"current_user_url":"https://api.github.com/user","current_user_authorizations_html_url":"https://github.com/settings/connections/applications{/client_id}","authorizations_url":"https://api.github.com/authorizations","code_search_url":"https://api.github.com/search/code?q={query}{&page,per_page,sort,order}","commit_search_url":"https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}","emails_url":"https://api.github.com/user/emails","emojis_url":"https://api.github.com/emojis","events_url":"https://api.github.com/events","feeds_url":"https://api.github.com/feeds","followers_url":"https://api.github.com/user/followers","following_url":"https://api.github.com/user/following{/target}","gists_url":"https://api.github.com/gists{/gist_id}","hub_url":"https://api.github.com/hub","issue_search_url":"https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}","issues_url":"https://api.github.com/issues","keys_url":"https://api.github.com/user/keys","notifications_url":"https://api.github.com/notifications","organization_repositories_url":"https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}","organization_url":"https://api.github.com/orgs/{org}","public_gists_url":"https://api.github.com/gists/public","rate_limit_url":"https://api.github.com/rate_limit","repository_url":"https://api.github.com/repos/{owner}/{repo}","repository_search_url":"https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}","current_user_repositories_url":"https://api.github.com/user/repos{?type,page,per_page,sort}","starred_url":"https://api.github.com/user/starred{/owner}{/repo}","starred_gists_url":"https://api.github.com/gists/starred","team_url":"https://api.github.com/teams","user_url":"https://api.github.com/users/{user}","user_organizations_url":"https://api.github.com/user/orgs","user_repositories_url":"https://api.github.com/users/{user}/repos{?type,page,per_page,sort}","user_search_url":"https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"}'
    #con login b'{"login":"jlbmdm","id":7573380,"node_id":"MDQ6VXNlcjc1NzMzODA=","avatar_url":"https://avatars2.githubusercontent.com/u/7573380?v=4","gravatar_id":"","url":"https://api.github.com/users/jlbmdm","html_url":"https://github.com/jlbmdm","followers_url":"https://api.github.com/users/jlbmdm/followers","following_url":"https://api.github.com/users/jlbmdm/following{/other_user}","gists_url":"https://api.github.com/users/jlbmdm/gists{/gist_id}","starred_url":"https://api.github.com/users/jlbmdm/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/jlbmdm/subscriptions","organizations_url":"https://api.github.com/users/jlbmdm/orgs","repos_url":"https://api.github.com/users/jlbmdm/repos","events_url":"https://api.github.com/users/jlbmdm/events{/privacy}","received_events_url":"https://api.github.com/users/jlbmdm/received_events","type":"User","site_admin":false,"name":"Jose","company":null,"blog":"","location":"Spain","email":null,"hireable":null,"bio":null,"public_repos":9,"public_gists":0,"followers":0,"following":10,"created_at":"2014-05-13T19:44:41Z","updated_at":"2019-08-30T16:09:38Z","private_gists":0,"total_private_repos":0,"owned_private_repos":0,"disk_usage":0,"collaborators":0,"two_factor_authentication":false,"plan":{"name":"free","space":976562499,"collaborators":0,"private_repos":10000}}'

    print('prueba2 text:   ', response2.text)
    #sin login {"current_user_url":"https://api.github.com/user","current_user_authorizations_html_url":"https://github.com/settings/connections/applications{/client_id}","authorizations_url":"https://api.github.com/authorizations","code_search_url":"https://api.github.com/search/code?q={query}{&page,per_page,sort,order}","commit_search_url":"https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}","emails_url":"https://api.github.com/user/emails","emojis_url":"https://api.github.com/emojis","events_url":"https://api.github.com/events","feeds_url":"https://api.github.com/feeds","followers_url":"https://api.github.com/user/followers","following_url":"https://api.github.com/user/following{/target}","gists_url":"https://api.github.com/gists{/gist_id}","hub_url":"https://api.github.com/hub","issue_search_url":"https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}","issues_url":"https://api.github.com/issues","keys_url":"https://api.github.com/user/keys","notifications_url":"https://api.github.com/notifications","organization_repositories_url":"https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}","organization_url":"https://api.github.com/orgs/{org}","public_gists_url":"https://api.github.com/gists/public","rate_limit_url":"https://api.github.com/rate_limit","repository_url":"https://api.github.com/repos/{owner}/{repo}","repository_search_url":"https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}","current_user_repositories_url":"https://api.github.com/user/repos{?type,page,per_page,sort}","starred_url":"https://api.github.com/user/starred{/owner}{/repo}","starred_gists_url":"https://api.github.com/gists/starred","team_url":"https://api.github.com/teams","user_url":"https://api.github.com/users/{user}","user_organizations_url":"https://api.github.com/user/orgs","user_repositories_url":"https://api.github.com/users/{user}/repos{?type,page,per_page,sort}","user_search_url":"https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"}
    #con login {"login":"jlbmdm","id":7573380,"node_id":"MDQ6VXNlcjc1NzMzODA=","avatar_url":"https://avatars2.githubusercontent.com/u/7573380?v=4","gravatar_id":"","url":"https://api.github.com/users/jlbmdm","html_url":"https://github.com/jlbmdm","followers_url":"https://api.github.com/users/jlbmdm/followers","following_url":"https://api.github.com/users/jlbmdm/following{/other_user}","gists_url":"https://api.github.com/users/jlbmdm/gists{/gist_id}","starred_url":"https://api.github.com/users/jlbmdm/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/jlbmdm/subscriptions","organizations_url":"https://api.github.com/users/jlbmdm/orgs","repos_url":"https://api.github.com/users/jlbmdm/repos","events_url":"https://api.github.com/users/jlbmdm/events{/privacy}","received_events_url":"https://api.github.com/users/jlbmdm/received_events","type":"User","site_admin":false,"name":"Jose","company":null,"blog":"","location":"Spain","email":null,"hireable":null,"bio":null,"public_repos":9,"public_gists":0,"followers":0,"following":10,"created_at":"2014-05-13T19:44:41Z","updated_at":"2019-08-30T16:09:38Z","private_gists":0,"total_private_repos":0,"owned_private_repos":0,"disk_usage":0,"collaborators":0,"two_factor_authentication":false,"plan":{"name":"free","space":976562499,"collaborators":0,"private_repos":10000}}

    print('prueba2 json:   ', response1.json)
    #sin login <bound method Response.json of <Response [200]>>
    #con login <bound method Response.json of <Response [200]>>
    input('Pulsa un tecla 2')
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#Pruebas de conexion a Internet con login opcion 2 -> creando una sesión
if False:
    mi_usuario = 'jbengoam@gmail.com'
    # By using a context manager, you can ensure the resources used by
    # the session will be released after use
    print(f'Para el siguiente requests se solicita contraseña de github.com para el usuario {mi_usuario}')
    with requests.Session() as session:
        session.auth = (mi_usuario, getpass())
        # Instead of requests.get(), you'll use session.get()
        response3 = session.get('https://api.github.com/user')
    # You can inspect the response just like you did before
    print('prueba3:', response3)
    print('prueba3 text:   ', response3.text)
    #sin login0 {"current_user_url":"https://api.github.com/user","current_user_authorizations_html_url":"https://github.com/settings/connections/applications{/client_id}","authorizations_url":"https://api.github.com/authorizations","code_search_url":"https://api.github.com/search/code?q={query}{&page,per_page,sort,order}","commit_search_url":"https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}","emails_url":"https://api.github.com/user/emails","emojis_url":"https://api.github.com/emojis","events_url":"https://api.github.com/events","feeds_url":"https://api.github.com/feeds","followers_url":"https://api.github.com/user/followers","following_url":"https://api.github.com/user/following{/target}","gists_url":"https://api.github.com/gists{/gist_id}","hub_url":"https://api.github.com/hub","issue_search_url":"https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}","issues_url":"https://api.github.com/issues","keys_url":"https://api.github.com/user/keys","notifications_url":"https://api.github.com/notifications","organization_repositories_url":"https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}","organization_url":"https://api.github.com/orgs/{org}","public_gists_url":"https://api.github.com/gists/public","rate_limit_url":"https://api.github.com/rate_limit","repository_url":"https://api.github.com/repos/{owner}/{repo}","repository_search_url":"https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}","current_user_repositories_url":"https://api.github.com/user/repos{?type,page,per_page,sort}","starred_url":"https://api.github.com/user/starred{/owner}{/repo}","starred_gists_url":"https://api.github.com/gists/starred","team_url":"https://api.github.com/teams","user_url":"https://api.github.com/users/{user}","user_organizations_url":"https://api.github.com/user/orgs","user_repositories_url":"https://api.github.com/users/{user}/repos{?type,page,per_page,sort}","user_search_url":"https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"}
    #con login1 {"login":"jlbmdm","id":7573380,"node_id":"MDQ6VXNlcjc1NzMzODA=","avatar_url":"https://avatars2.githubusercontent.com/u/7573380?v=4","gravatar_id":"","url":"https://api.github.com/users/jlbmdm","html_url":"https://github.com/jlbmdm","followers_url":"https://api.github.com/users/jlbmdm/followers","following_url":"https://api.github.com/users/jlbmdm/following{/other_user}","gists_url":"https://api.github.com/users/jlbmdm/gists{/gist_id}","starred_url":"https://api.github.com/users/jlbmdm/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/jlbmdm/subscriptions","organizations_url":"https://api.github.com/users/jlbmdm/orgs","repos_url":"https://api.github.com/users/jlbmdm/repos","events_url":"https://api.github.com/users/jlbmdm/events{/privacy}","received_events_url":"https://api.github.com/users/jlbmdm/received_events","type":"User","site_admin":false,"name":"Jose","company":null,"blog":"","location":"Spain","email":null,"hireable":null,"bio":null,"public_repos":9,"public_gists":0,"followers":0,"following":10,"created_at":"2014-05-13T19:44:41Z","updated_at":"2019-08-30T16:09:38Z","private_gists":0,"total_private_repos":0,"owned_private_repos":0,"disk_usage":0,"collaborators":0,"two_factor_authentication":false,"plan":{"name":"free","space":976562499,"collaborators":0,"private_repos":10000}}
    #con login2 {"login":"jlbmdm","id":7573380,"node_id":"MDQ6VXNlcjc1NzMzODA=","avatar_url":"https://avatars2.githubusercontent.com/u/7573380?v=4","gravatar_id":"","url":"https://api.github.com/users/jlbmdm","html_url":"https://github.com/jlbmdm","followers_url":"https://api.github.com/users/jlbmdm/followers","following_url":"https://api.github.com/users/jlbmdm/following{/other_user}","gists_url":"https://api.github.com/users/jlbmdm/gists{/gist_id}","starred_url":"https://api.github.com/users/jlbmdm/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/jlbmdm/subscriptions","organizations_url":"https://api.github.com/users/jlbmdm/orgs","repos_url":"https://api.github.com/users/jlbmdm/repos","events_url":"https://api.github.com/users/jlbmdm/events{/privacy}","received_events_url":"https://api.github.com/users/jlbmdm/received_events","type":"User","site_admin":false,"name":"Jose","company":null,"blog":"","location":"Spain","email":null,"hireable":null,"bio":null,"public_repos":9,"public_gists":0,"followers":0,"following":10,"created_at":"2014-05-13T19:44:41Z","updated_at":"2019-08-30T16:09:38Z","private_gists":0,"total_private_repos":0,"owned_private_repos":0,"disk_usage":0,"collaborators":0,"two_factor_authentication":false,"plan":{"name":"free","space":976562499,"collaborators":0,"private_repos":10000}}
    input('Pulsa un tecla 3')
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#Prueba de incluir data en el post
if False:
    try:
        rpta1 = requests.post('https://httpbin.org/post', data={'key':'value'})
        rpta1.raise_for_status()
    except:
        print('requests post error')
    else:
        print('API KEY ok')
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#Descarga de iagen radar, verificando la respuesta
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
if False:
    try:
        rpta1 = requests.get(urlRadarPalenciaAPIKEY, headers={'Accept': 'application/json', 'api_key': APY_KEY})
        #El codigo de AEMET pasa el API_KEY como parametro en vez de como headers:
        #rpta2 = requests.get(urlRadarPalenciaAPIKEY, headers={}, params={'api_key': APY_KEY}, verify=False)
        rpta1.raise_for_status()
    except HTTPError as http_err:
        print('\nError en requests accediendo:', urlRadarPalenciaAPIKEY)
        print(f'HTTP error occurred: {http_err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
    except Exception as err:
        print('\nError en requests accediendo:', urlRadarPalenciaAPIKEY)
        print(f'Other error occurred: {err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
    else:
        #print('Rpta al API KEY', rpta1.headers)
        #print('Rpta al API KEY1', rpta1.text)
        #print('Rpta al API KEY2', rpta1.json())
        #for item in rpta1.json():
        #    print('  ', item, '->', rpta1.json()[item])
        if rpta1.json()['descripcion'] =="exito" or rpta1.json()["estado"] == 200:
            ahora = datetime.datetime.now() #<class 'datetime.datetime'>
            print(ahora, 'Respuesta de la API de opendata.aemet.es: API KEY ok')
            miUrl2 = rpta1.json()['datos']
        elif rpta1.json()['descripcion'] =="datos expirados" or rpta1.json()["estado"] == 404:
            print('API KEY incorrecta')
            quit()
        else:
            print('Revisar http')
            continue
    
    try:
        rpta2 = requests.get(miUrl2)
        rpta2.raise_for_status()
    except HTTPError as http_err:
        print('\nError en requests accediendo:', miUrl2)
        print(f'HTTP error occurred: {http_err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
    except Exception as err:
        print('\nError en requests accediendo:', miUrl2)
        print(f'Other error occurred: {err}')  # Python 3.6 -> ver: https://realpython.com/python-f-strings/
    else:
        #print('Rpta al API KEY', rpta2.headers)
        #print('->', rpta2.content)
    
        if False:
            for header in rpta2.headers:
                print('\t', header, '\t->', rpta2.headers[header])
            #print('\nrpta2.cookies:\t',rpta2.cookies)
        
        print('Contenido devuelto por AEMET:', rpta2.headers['Content-Type'], 'tamaño:', rpta2.headers['Content-Length'], type(rpta2.content))
        print('Consulta:', rpta2.headers['aemet_num'], 'Consultas restantes:', rpta2.headers['Remaining-request-count'])
        ahora = str(datetime.datetime.now()).replace(' ', '_').replace(':', 'h')[:16]
        rutaImagenes = os.path.abspath(r'../data/tormetron/')
        miImagen = f'{rutaImagenes}/AEMET_radar_Palencia_{ahora}.gif'
        #miImagenSinRuta = os.path.splitext(os.path.basename(miImagen))[0]
        if os.path.exists(miImagen):
            print('La imagen', miImagen, 'ya existe')
            time.sleep(60)
            continue
        if rpta2.headers['Content-Type'][:9] == 'image/gif':
            try:
                myImage = open(miImagen, 'wb')
                myImage.write(rpta2.content)
                myImage.close()
                print('Se ha creado una nueva imagen', miImagen, 'de', os.path.getsize(miImagen), 'bytes', 'bytes', end='')
            except:
                print('Error 2 - imagen no guardada', miImagen)

            georeferenciarImagenRadar(miImagen)

        elif rpta2.headers['Content-Type'][:16] == 'application/json':
            print('Imagen no disponible')
        else:
            print('-->', rpta2.headers['Content-Type'][:16])
    time.sleep(60*10)

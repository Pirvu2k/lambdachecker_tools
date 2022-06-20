import requests
from getpass import getpass

api_url = 'https://apibeta.lambdachecker.io'

endpoints = {
    'login': f'{api_url}/users/login',
    'submissions': f'{api_url}/user-subm', # in reality returns best submission for each problem
    'problem_info': f'{api_url}/problems/{{id}}?contest_id=-1' # double curly used for format strings
}

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def login():
    teacher_username = input('Lambdachecker teacher username: ')
    teacher_password = getpass('Lambdachecker teacher password: ')

    login_request = {
        'email': teacher_username,
        'password': teacher_password,
        'facebookLogin': False
    }

    try:
        resp = requests.post(endpoints['login'], login_request)
        resp.raise_for_status()
        
        resp = resp.json()

        if 'error' in resp:
            raise SystemExit(resp['error'])

    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)
    
    return resp['token']

def get_problem_info(problem_id, token):
    try:
        resp = requests.get(endpoints['problem_info'].format(id = problem_id), auth=BearerAuth(token))
        resp.raise_for_status()
        
        return resp.json()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)
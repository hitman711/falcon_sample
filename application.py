from datetime import datetime
import falcon
import json
import requests
import urllib

GITHUB_API = 'https://api.github.com/search/repositories'
GITHUB_COMMIT_API = 'https://api.github.com/repos/{}/commits?per_page=1'


def last_commit_response(repository_full_name):
    """ Fetch latest commit information for given repository name"""
    return_obj = {
        'sha':'',
        'commit_message': '',
        'commit_author_name': ''
    }
    try:
        response = requests.get(
            GITHUB_COMMIT_API.format(repository_full_name), timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response:
                return_obj['sha'] = response[0]['sha']
                return_obj['commit_message'] = response[0]['commit']['message']
                return_obj['commit_author_name'] = response[0]['commit']['author']['name']
            return return_obj
        else:
            return return_obj    
    except Exception as e:
        return return_obj

class GitSearch(object):
    """ API endpoint to fetch repository information based on search param"""
    
    def on_get(self, req, resp):
        """ """
        return_obj = []
        search_param = {
            'q': req.params.get('search_term'),
            'sort':'created',
            'order':'desc'
        }
        if not search_param['q']:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(
                {
                    'message': 'Invalid search paramter',
                    'errors':{
                        'search_param': 'Please provide valid search parameter'
                    }
                }
            )
        else:
            query_param = urllib.parse.urlencode(search_param)
            url = GITHUB_API +'?'+ query_param
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    response = response.json()['items']
                    if response:
                        response.sort(
                            key=lambda item: datetime.strptime(
                                item['created_at'], "%Y-%m-%dT%H:%M:%SZ"
                            ), reverse=True)
                        for x in response[:5]:
                            response_obj = {
                                'respository_name': x['name'],
                                'created_at': x['created_at'],
                                'owner_url': x['owner']['url'],
                                'avatar_url': x['owner']['avatar_url']
                            }
                            response_obj.update(
                                last_commit_response(
                                    x['full_name']
                                )
                            )
                            return_obj.append(response_obj)

                        resp.status = falcon.HTTP_200
                        resp.body = json.dumps(return_obj)
                    else:
                        resp.status = falcon.HTTP_200
                        resp.body = json.dumps([])
                else:
                    resp.status = str(response.status_code)
                    resp.body = response.json(response.json())
            except Exception as e:
                resp.status = falcon.HTTP_500
                resp.body = json.dumps(
                    {
                        'message': 'API reponse timeout',
                        'non_field_error':['Github api response time out.']
                    }
                )

class Index(object):
    """ """
    
    def on_get(self, req, resp):
        """End point to provide html template"""
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open('template.html', 'r') as f:
            resp.body = f.read()

api = falcon.API()
api.add_route('/', Index())
api.add_route('/api', GitSearch())
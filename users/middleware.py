import fetch

def get_user(request):
    if 'username' in request.session:
        try:
            user = fetch.get_user_by_username(request.session['username'])
            return {
                'username': user.username,
                'password': user.password,
                'is_authenticated': True
            }
        except fetch.DatabaseError:
            pass
    return {
        'password': None,
        'is_authenticated': False,
    }

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            request._cached_user = get_user(request)
        return request._cached_user

class UserMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()

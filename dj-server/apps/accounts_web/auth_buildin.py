from django.contrib.auth import authenticate


class BuildinAuthHelper(object):

    def __init__(self, config):
        super(BuildinAuthHelper, self).__init__()

    def get_user_info(self, user_name, password):
        user = authenticate(username=user_name, password=password)
        if user:
            params = {}
            params['full_name'] = '{0} {1}'.format(
                user.first_name,
                user.last_name,
            )
            params['user_name'] = user.username
            return params
        return None

    def auth(self, user_name, password):
        user = authenticate(username=user_name, password=password)
        if user:
            return True
        return False

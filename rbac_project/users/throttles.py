from rest_framework.throttling import SimpleRateThrottle

class LoginThrottle(SimpleRateThrottle):
    scope = 'login'

    def get_cache_key(self, request, view):
        # Use the user's IP address for throttling unauthenticated requests
        return self.get_ident(request)

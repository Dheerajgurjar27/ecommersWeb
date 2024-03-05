from django.shortcuts import redirect

def auth_middleware(get_response):


    def middleware(request):
        retrurnUrl = request.META['PATH_INFO']

        if not request.session.get('customer'):
            return redirect(f'loginpage?retrun_url={retrurnUrl}')

        response = get_response(request)
        return response
    
    return middleware

# f'loginpage?retrun_url{retrurnUrl}'
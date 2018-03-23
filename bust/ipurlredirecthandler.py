from urllib import request

class IpUrlRedirectHandler(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        """@TODO: Rewrite the URL as required"""
        print(newurl)
        return super(IpUrlRedirectHandler, self).redirect_request(req, fp, code, msg, hdrs, newurl)

from urllib import request
from urllib.parse import urlparse, urljoin


class IpUrlRedirectHandler(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):

        if 'Host' not in req.headers:
            print('** redirect: '+newurl)
            return super(IpUrlRedirectHandler, self).redirect_request(
                req, fp, code, msg, hdrs, newurl
            )

        original_url = urlparse(req.get_full_url())
        new_url = urlparse(newurl)

        custom_url = urljoin(
            newurl,
            '//'+original_url.hostname
        )
        req.headers['Host'] = new_url.hostname

        print('** redirect: '+new_url.hostname+'@'+custom_url)
        return super(IpUrlRedirectHandler, self).redirect_request(
            req, fp, code, msg, hdrs, custom_url
        )

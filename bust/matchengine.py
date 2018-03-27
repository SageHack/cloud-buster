from ipv6support import IPv6Support
from reqcontent import RequestContent
from difflib import SequenceMatcher


class MatchEngine:
    def is_origin(cdn_host, origin_ip):

        cdn_url = 'http://'+cdn_host
        cdn_content = RequestContent(cdn_url).__get__()

        origin_url = 'http://'+IPv6Support.fix(origin_ip)
        origin_content = RequestContent(origin_url, cdn_host).__get__()

        if cdn_content['status'] != origin_content['status']:
            return False

        title_match = MatchEngine.compare(
            'title', cdn_content['title'], origin_content['title']
        )
        if title_match:
            return True

        html_match = MatchEngine.compare(
            'html', cdn_content['html'], origin_content['html']
        )
        if html_match:
            return True

        return False

    def compare(method, s1, s2):
        strings = [s1, s2]

        for s in strings:
            if not isinstance(s, str):
                return False
            if len(s) < 1:
                return False

        if strings[0] == strings[1]:
            print('!! %s match' % (method), flush=True)
            return True

        if len(s) > 10:
            similarity = SequenceMatcher(None, s1, s2).ratio()
            if similarity > 0.9:
                print('!! %s similar (%.2f)' % (method, similarity), flush=True)
                return True

        return False

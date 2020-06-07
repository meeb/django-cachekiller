import subprocess
from django.template import Library, Node
from django.utils.timezone import now
from urllib.parse import urlsplit, urlunsplit
from django.utils.encoding import force_text
from django.templatetags.static import do_static


register = Library()


class RepoRefCache(object):
    '''
        Simple reference state cache so the reference tags are only requested
        once.
    '''

    def __init__(self):
        self._git_tip = None
        self._git_failed = False
        self._hg_tip = None
        self._hg_failed = False

    def _run_cmd(self, cmd):
        try:
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            return None

    def _strip_ref(self, ref):
        first_word = ref.split(' ')[0]
        return first_word.replace('"', '').replace('\'', '').strip()

    def get_git_tip(self):
        if self._git_failed:
            return None
        elif self._git_tip:
            return self._git_tip[:14]
        ref = self._run_cmd(['git', 'rev-parse', 'HEAD'])
        ref = force_text(ref)
        if ref == 'None':
            self._git_failed = False
            return None
        else:
            self._git_tip = self._strip_ref(ref)
            return self._git_tip[:14]

    def get_hg_tip(self):
        if self._hg_failed:
            return None
        elif self._hg_tip:
            return self._hg_tip[:14]
        ref = self._run_cmd(['hg', 'heads', '--template', '"{node}"'])
        ref = force_text(ref)
        if ref == 'None':
            self._hg_failed = True
            return None
        else:
            self._hg_tip = self._strip_ref(ref)
            return self._hg_tip[:14]

    def get_ts(self):
        return now().strftime('%Y%m%d%H%M%S')

    def get_ref(self):
        ref = self.get_git_tip()
        if ref:
            return ref
        ref = self.get_hg_tip()
        if ref:
            return ref
        ref = self.get_ts()
        if ref:
            return ref
        return None


refcache = RepoRefCache()


class CDNStaticURLNode(Node):

    def __init__(self, url):
        self.url = url

    def render(self, context):
        url = self.url.render(context)
        parts = urlsplit(url)
        if parts.query:
            qs = parts.query + '&tag=' + refcache.get_ref()
        else:
            qs = 'tag=' + refcache.get_ref()
        return urlunsplit((parts.scheme, parts.netloc, parts.path, qs,
            parts.fragment))


@register.tag('cdnstatic')
def do_cdnstatic(parser, token):
    url = do_static(parser, token)
    return CDNStaticURLNode(url)

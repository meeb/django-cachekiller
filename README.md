# django-cachebuster

`django-cachebuster` is a small add-on for Django that adds the `cdnstatic`
template tag which adds a 'cache busting' dynamic query string appended to the
file paths. This tag functions identically to the standard `{% static ... %}`
template tag. This is designed to work with CDNs that cache by complete URI
including the query string so when you push a change the CDNs are automatically
refreshed without having to wait for TTLs to expire. Internally we use this with
`django-distill`, a static site generator for Django to work with static sites
with heavy caching on images behind CloudFlare, cachefly and other CDNs:

https://github.com/mgrp/django-distill

Under the hood, this module just chains the request to the existing `static` tag
to be widely compatible.

# Installation

Install from pip:

```bash
$ pip install --upgrade git+git://github.com/mgrp/django-cachebuster.git@master
```

Add `django_cachebuster` to your `INSTALLED_APPS` in your `settings.py`:

```python
INSTALLED_APPS += ('django_cachebuster',)
```

That's it. Once installed, all calls to the `static` template tag will be
intercepted and rewritten for you.

# Usage

Load the new module at the top of your templates:

```html
{% load cdnstaticfiles %}
```

Then use it in the template exactly as you would use the `static`:

```html
{% cdnstatic 'some/image.jpg' %}
```
This renders as (assuming `settings.STATIC_URL` is set to `/static/`):

```html
/static/some/image.jpg?tag=[random tag]
```

`[random tag]` is either the truncated mercurial or git commit reference if it
is available, otherwise it will be the current date in `YYYYMMDDHHMMSS` format.
If there are existing query string parameters then the `tag` is intelligently
appended. The `cdnstatic` tag will not break the existing URL.

# Contributing

All properly formatted and sensible pull requests, issues and comments are
welcome.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tornado Blueprint蓝图的实现。"""

import asyncio
import collections
import inspect
from concurrent.futures import ThreadPoolExecutor

import tornado.netutil
import tornado.process
import tornado.web
from tornado.options import define, options
from utils import Cache, Dict, Logger, get_ip

__all__ = ['Blueprint', 'Application']

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass


class BlueprintMeta(type):
    derived_class = []

    def __new__(cls, name, bases, attr):
        _class = super(BlueprintMeta, cls).__new__(cls, name, bases, attr)
        cls.derived_class.append(_class)
        return _class

    @classmethod
    def register(cls, app):
        for _class in cls.derived_class:
            for blueprint in _class.blueprints:
                app.register(blueprint)


class Blueprint(metaclass=BlueprintMeta):
    blueprints = []

    def __init__(self, name=None, url_prefix='/', host='.*', strict_slashes=False):
        self.name = name
        self.host = host
        self.rules = []
        self.url_prefix = url_prefix
        self.strict_slashes = strict_slashes
        self._events = collections.defaultdict(list)
        self.blueprints.append(self)

    def route(self, uri, params=None, name=None):
        def decorator(handler):
            assert uri[0] == '/'
            rule_name = name or handler.__name__
            if self.name:
                rule_name = f'{self.name}.{rule_name}'
            if rule_name in [x[-1] for x in self.rules]:
                rule_name = None
            rule_uri = self.url_prefix.rstrip('/') + uri
            self.rules.append((rule_uri, handler, params, rule_name))
            if not self.strict_slashes and rule_uri.endswith('/'):
                self.rules.append((rule_uri.rstrip('/'), handler, params, None))
            return handler
        return decorator

    def listen(self, event):
        def decorater(func):
            self._events[event].append(func)
        return decorater


class Application(Blueprint):

    define('debug', default=True, type=bool)
    define('port', default=8000, type=int)
    define('workers', default=1, type=int)

    def __init__(self, name=None, url_prefix='/', host='.*', strict_slashes=False, **kwargs):
        super().__init__(name, url_prefix, host, strict_slashes)
        self.prefix = 'web'
        self.logger = Logger()
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(10)
        self._cache = Cache()
        self._kwargs = Dict(kwargs)
        self._handlers = []
        self._events = collections.defaultdict(list)

        options.parse_command_line()
        self.opt = Dict(options.items())

    def register(self, *blueprints, url_prefix='/'):
        assert url_prefix[0] == '/'
        url_prefix = url_prefix.rstrip('/')
        for blueprint in blueprints:
            rules = [(url_prefix + x[0], *x[1:]) for x in blueprint.rules]
            self._handlers.append((blueprint.host, rules))
            for rule in rules:
                setattr(rule[1], 'app', self)
            if blueprint != self:
                for k, v in blueprint._events.items():
                    self._events[k].extend(v)

    def url_for(self, endpoint, *args, **kwargs):
        return self.app.reverse_url(endpoint, *args, **kwargs)

    def make_app(self):
        app = tornado.web.Application(**self._kwargs)
        for host, rules in self._handlers:
            app.add_handlers(host, rules)
        return app

    async def shutdown(self):
        self.logger.info('shutting down')
        self.server.stop()
        # tasks = [x for x in asyncio.Task.all_tasks() if x is not asyncio.tasks.Task.current_task()]
        # self.logger.warning(f'canceling {len(tasks)} pending tasks')
        # if tasks:
        #     asyncio.gather(*tasks, return_exceptions=True).cancel()
        self.loop.stop()

    async def main(self):
        if hasattr(self, 'init'):
            ret = self.init()
            if inspect.isawaitable(ret):
                await ret

        for func in self._events['startup']:
            ret = func(self)
            if inspect.isawaitable(ret):
                await ret

        self.register(self)
        app = tornado.web.Application(**self._kwargs)
        for host, rules in self._handlers:
            app.add_handlers(host, rules)

        self.server = app.listen(options.port)
        await asyncio.Event().wait()

    def run(self):
        self._kwargs.setdefault('static_path', 'static')
        self._kwargs.setdefault('template_path', 'templates')
        self._kwargs.setdefault('cookie_secret', 'YWpzYWhkaDgyMTgzYWpzZGphc2RhbDEwMjBkYWph')
        self._kwargs.setdefault('xsrf_cookie', True)
        self._kwargs.setdefault('login_url', '/signin')
        self._kwargs.setdefault('xheaders', True)
        self._kwargs.setdefault('debug', options.debug)

        # self.loop.add_signal_handler(signal.SIGTERM, self.shutdown)
        # self.loop.add_signal_handler(signal.SIGINT, self.shutdown)

        self.logger.info(f"Debug: {self.opt.debug}, Address: http://{get_ip()}:{self.opt.port}")
        asyncio.run(self.main())

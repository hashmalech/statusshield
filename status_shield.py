class StatusError:
    handle_errors = {}

    def __init__(self, app):
        self.app = app
        self.status_error = None

    def __call__(self, environ, start_response):
        self.start_response = start_response
        response = self.app(environ, self.intercept_response)
        if self.status_error:
            try: out = str(self.handle_errors[self.status_error]())
            except KeyError: out = ''
            return [out]
        return response

    def intercept_response(self, status, headers, exc_info=None):
        status_code = int(status[0])
        if status_code in [4, 5]:
            self.status_error = int(status[:3])
        # TODO: don't overwrite existing headers
        headers = [('Content-Type', 'text/html; charset=UTF-8')]
        return self.start_response(status, headers, exc_info)

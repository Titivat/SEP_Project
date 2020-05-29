import msgpack

class Response(object):
    """Default template for all server response"""

    def __init__(self, ctx):
        self.ctx = ctx
    
    def __call__(self, success=True, **kwargs):
        response = {"ctx": self.ctx, "success": success}
        for k, v in kwargs.items():
            response[k] = v
        return msgpack.packb(response)

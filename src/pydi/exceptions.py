class NotAClassException(ValueError):
    def __init__(self, name: str):
        super().__init__("this '%s' is not a Class" % name)


class MissingArgumentException(ValueError):
    def __init__(self, arg_name: str):
        super().__init__("missing '%s'" % arg_name)


class NotAPyDIModule(ValueError):
    def __init__(self, name: str):
        super().__init__("this: %s, not a pydi module" % name)


class NotAPyDIProvider(ValueError):
    def __init__(self, name: str):
        super().__init__("this: %s, not a pydi provider" % name)


class AnnotationsNotSupported(TypeError):
    def __init__(self, name: str):
        super().__init__("this: %s, not support annotations" % name)


class CannotResolveDependency(RuntimeError):
    def __init__(self, dep_name: str, at: str):
        super().__init__("Cannot resolve %s at %s" % (dep_name, at))

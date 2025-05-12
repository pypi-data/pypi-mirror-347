# pyvenDF/router.py

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, pattern, handler):
        self.routes.append((pattern, handler))

    def match(self, path):
        for pattern, handler in self.routes:
            if self.path_matches(pattern, path):
                return handler, self.extract_parameters(pattern, path)
        return None, None

    def path_matches(self, pattern, path):
        if pattern.count(".") == 1:
            base_path = pattern.split(".")[0]
            return path.startswith(base_path)
        return False

    def extract_parameters(self, pattern, path):
        if pattern.count(".") == 1:
            base_path = pattern.split(".")[0]
            param_value = path[len(base_path)+1:]
            return {"id": param_value}
        return {}

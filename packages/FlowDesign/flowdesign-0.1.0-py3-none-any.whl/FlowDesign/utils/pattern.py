import threading

class Factory:
    _registry = {}

    @classmethod
    def register_class(cls, key):
        def wrapper(obj):
            cls._registry[key] = obj
            return obj
        return wrapper

    @classmethod
    def get_instance(cls, key, *args, **kwargs):
        if key not in cls._registry: raise ValueError(f"Class with key '{key}' is not registered.")
        return cls._registry[key](*args, **kwargs)

class OnlyInstance:
    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self
    
class Future:
    def __init__(self):
        self._result = None
        self._event = threading.Event()
    
    def set_result(self, result):
        self._result = result
        self._event.set()
    
    def get_result(self):
        self._event.wait()
        return self._result

class Batcher:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.isworking = False
    
    def __call__(self, request_data):
        future = Future()
        with self.lock:
            self.buffer.append((request_data, future))
            if self.isworking == False:
                threading.Thread(target=self.process).start()
        return future.get_result()
    
    def process(self):
        with self.lock:
            if not self.buffer: return
            self.isworking = True
            current_buffer = self.buffer
            self.buffer = []
        
        requests = [req for req, fut in current_buffer]
        responses = self.run(requests, batch=True)
        
        for (_, future), response in zip(current_buffer, responses):
            future.set_result(response)

        with self.lock:
            self.isworking = False
            if self.buffer:
                threading.Thread(target=self.process).start()


# class Batcher:
#     def __init__(self):
#         self.buffer = []
#         self.lock = threading.Lock()
#         self.is_working = False
#         self.cv = threading.Condition(self.lock)  # Add condition variable

#     def __call__(self, request_data):
#         with self.lock:
#             future = Future()
#             self.buffer.append((request_data, future))

#             if not self.is_working:
#                 self.is_working = True
#                 threading.Thread(target=self.process).start()

#             return future.get_result()

#     def process(self):
#         while True:
#             with self.lock:
#                 if not self.buffer:
#                     self.is_working = False
#                     return
                
#                 current_buffer = self.buffer
#                 self.buffer = []

#             # Process current buffer
#             requests = [req for req, fut in current_buffer]
#             responses = self.run(requests, batch=True)  # Implement your batch processing
            
#             # Set results
#             for (_, future), response in zip(current_buffer, responses):
#                 future.set_result(response)
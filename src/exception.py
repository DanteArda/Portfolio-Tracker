class BadStatusCodeError(Exception):
    """Returns an error if the API response returns a status code other than 200"""
    def __init__(self, status_code : int):
        def return_status_code_message():
            match self.status_code:
                case 200: return "OK; You most likely did not intend for this to happen"
                case 400: return "Invalid"
                case 401: return "Bad API key"
                case 403: return "Scope missing for API key"
                case 404: return "Not found"
                case 408: return "Timed-Out"
                case 429: return "Limited"
                case _: return "Unknown"

        self.status_code = status_code
        self.message = return_status_code_message()

        super().__init__(f"{self.status_code}: {self.message}")
        
class PrematureEvaluationError(Exception):
    """Returns an error if a required variable isn't assigned before being evaluated"""
    def __init__(self, variable, cls):
        self.variable = variable
        self.class_name = cls.__class__.__name__
        super().__init__(f"{self.class_name}.{self.variable} must be assigned before being evaluated")
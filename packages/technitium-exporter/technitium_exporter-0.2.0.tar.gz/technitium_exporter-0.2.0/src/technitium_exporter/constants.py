import re

UPDATE_CHECK_URI = "/api/user/checkForUpdate"
STATS_URI = "/api/dashboard/stats/get"
CAMEL_CASE = re.compile(r'(?<!^)(?=[A-Z])')

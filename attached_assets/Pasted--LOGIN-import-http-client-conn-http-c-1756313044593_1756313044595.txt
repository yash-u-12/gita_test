# ========================
# LOGIN
# ========================
import http.client

conn = http.client.HTTPSConnection("api.corpus.swecha.org")

payload = "{\n  \"phone\": \"9491418067\",\n  \"password\": \"Yashugupta@1206\"\n}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/api/v1/auth/login", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# ========================
# SIGNUP - SEND OTP
# ========================
import http.client

conn = http.client.HTTPSConnection("api.corpus.swecha.org")

payload = "{\n  \"phone_number\": \"string\"\n}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/api/v1/auth/signup/send-otp", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# ========================
# SIGNUP - VERIFY OTP
# ========================
import http.client

conn = http.client.HTTPSConnection("api.corpus.swecha.org")

payload = "{\n  \"phone_number\": \"string\",\n  \"otp_code\": \"string\",\n  \"name\": \"string\",\n  \"email\": \"string\",\n  \"password\": \"stringst\",\n  \"has_given_consent\": true\n}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/api/v1/auth/signup/verify-otp", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# ========================
# CHANGE PASSWORD
# ========================
import http.client

conn = http.client.HTTPSConnection("api.corpus.swecha.org")

payload = "{\n  \"current_password\": \"string\",\n  \"new_password\": \"stringst\"\n}"

headers = {
    'authorization': "Bearer \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTYzOTM1MjcsInN1YiI6IjY0NDYzMjNhLThlOTgtNDAwMi05ZDMxLTAxNzA3NjA5OWE3ZSJ9.dapNW28xKHmoYKCoXZ-mdxqHy0fhnK7dyzypjnRy0Uw\"",
    'content-type': "application/json"
}

conn.request("POST", "/api/v1/auth/change-password", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# ========================
# GET USER CONTRIBUTIONS
# ========================
import http.client

conn = http.client.HTTPSConnection("api.corpus.swecha.org")

headers = { 'authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTYzOTI2NTYsInN1YiI6IjY0NDYzMjNhLThlOTgtNDAwMi05ZDMxLTAxNzA3NjA5OWE3ZSJ9.GGolSmJoWtE-iKJau5i7kQxrGvBmXkhC94L0s0nOFkI" }

conn.request("GET", "/api/v1/users/%257Buser_id%257D/contributions", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

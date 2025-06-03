import requests
import json

# Define the base URL for the API
BASE_URL = "http://localhost:8000/api/report_stream/a4de72ba14357c555b3a2d986750cda5/"



# Function to make a POST request with valid data
def test_post_request():
    valid_data = {
        "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImU4NjNmZTI5MmZhMmEyOTY3Y2Q3NTUxYzQyYTEyMTFiY2FjNTUwNzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1MjIzNDU5ODgyNDUtbDFuZm85aWNxODJlaTVmaXJkbWkwaDFpcDdncXJwZjcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1MjIzNDU5ODgyNDUtbDFuZm85aWNxODJlaTVmaXJkbWkwaDFpcDdncXJwZjcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDAxNTcyNjc2NzQwMjUzNDExNjMiLCJlbWFpbCI6InRvdXFlZXJzaGFoMzJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5iZiI6MTczMTE4MTgxOSwibmFtZSI6InRvdXFlZXIgc2hhaCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMQWtmWllWX0pXamN0Y2hndnhBRjNpTGRHdHV2d25mNUtpS0VIVlYzQWhzNXBDTjEzejF3PXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6InRvdXFlZXIiLCJmYW1pbHlfbmFtZSI6InNoYWgiLCJpYXQiOjE3MzExODIxMTksImV4cCI6MTczMTE4NTcxOSwianRpIjoiM2Q3ZGU1NWM0NTkxMDFiOTFlZTM1MmY1NzgyMDBhOTQzZmMyNDA4MyJ9.FDATtEB2Ckvp6WIZqSJl-HqVP7yuboOTS2wCZlJ1yqlGwYEYvwfPGgC-XjcEogWaMHOEWtrPms9aJ-OwJSDZLhL6fMcGbABkaWztDAMZKCBPZ7LW_9mPyxKJaIkJgnxw-rwPgrgIFE5RYVl5bZrGjKmlVcH8Ljf6pNRo0pGyoo2E1gEZCYYMSaoNNOT55wYpNUNdJT1L5MVpftbnTwJ8XhTMLow9igKLPYibYP_eVmmpNLQFG3ihWgNtFRvXMReaUhkvvKZWjWA-OAqTUHOsdNmpytU8biXdwemY3BGTrnpAqcAbW9yFEt3PEc0Hrcdez9Mc-zFwxLf9R_ROLID2hQ",  # Replace with a real or mocked token for testing
        "query": "How to secure smart contracts?",
        "is_memory": False,
        "chat_id":"ssssss",
        "collections": [],
        "code_instruction":""
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL, data=json.dumps(valid_data), headers=headers)
    
    print("\nPOST request with valid data:")
    print("Status Code:", response.status_code)
    try:
        print("Response:", response.text)
    except json.JSONDecodeError:
        print("Response is not JSON format. Possibly a streamed response.")



# Call the functions to test the API
# test_get_request()
test_post_request()
# test_post_request_invalid_json()

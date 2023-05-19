from trycourier import Courier
client = Courier(auth_token="pk_test_DDKR2Q0F8C4VM5JYPDDPXRRWCCXW")
web_url="https://8000-cs-513293748685-default.cs-asia-southeast1-ajrg.cloudshell.dev"

def send_verification_link(email,token):
    resp = client.send_message(
        message={
            "to": {
            "email": f"{email}",
            },
            "template": "8FNSMHKQD7MC7TP6QSN494619NEQ",
            "data": {
            "username": f"{'username'}",
            "link": f"{web_url}/verify/{token}",
            },
        }
        )
def send_reset_link(email,username,token):
    resp = client.send_message(
        message={
            "to": {
            "email": f"{email}",
            },
            "template": "1C8M80SH1T4SNSN10H28X7P26C3W",
            "data": {
                "link": f"{web_url}/reset/{token}",
                "username":f"{username}"
            },
        }
        )
    print(resp)

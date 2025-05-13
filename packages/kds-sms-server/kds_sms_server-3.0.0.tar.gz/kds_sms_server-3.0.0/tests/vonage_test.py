from vonage import Vonage, Auth
from vonage_sms import SmsMessage, SmsResponse

if __name__ == '__main__':
    # Create an Auth instance
    auth = Auth(api_key="4e39cdea", api_secret="dx0NZNc69Kuf16Qx")

    # Create HttpClientOptions instance
    # (not required unless you want to change options from the defaults)
    # options = HttpClientOptions(api_host='api.nexmo.com', timeout=30)

    # Create a Vonage instance
    vonage = Vonage(auth=auth)

    message = SmsMessage(to="+4917680443353", from_='KDS TEST', text='Hello, World!')
    response: SmsResponse = vonage.sms.send(message)

    print(response.model_dump(exclude_unset=True))

    print()


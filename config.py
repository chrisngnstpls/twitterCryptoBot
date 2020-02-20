import twitter

def getApi():
    return twitter.Api(consumer_key='YOURCONSUMERKEY',
                       consumer_secret='YOURCONSUMERSECRET',
                       access_token_key='YOUTACCESSTOKENKEY',
                       access_token_secret='YOURACCESSTOKENSECRET')
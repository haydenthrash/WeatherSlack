import os
import time
import slack_auth
from slackclient import SlackClient

BOT_ID = slack_auth.BOT_ID

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMAND = "do"

slack_client = SlackClient(slack_auth.SLACK_BOT_TOKEN)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def handle_command(command, channel):
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMAND + \
                "* command ith numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel, text = response, as_user=True)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed.")

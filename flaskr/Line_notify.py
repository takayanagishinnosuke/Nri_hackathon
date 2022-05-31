import requests


def main(msg):
    send_line_notify(msg)

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = 'C6PXIUkkHkrDYnpZAdqvxFJzseMMTcpIO8F6udZl9Yg'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'報告: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    main()


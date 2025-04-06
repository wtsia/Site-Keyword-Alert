import requests
import time
import argparse
import re
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(sender_email, sender_password, recipient_email, subject, body):
    # Create the MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server (using Gmail as an example)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Email alert sent.")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to send email: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Monitor a woot.com page for a specific keyword and send an email alert when found."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL of the woot.com page to monitor (e.g., https://www.woot.com/category/electronics/other-electronics?ref=w_cnt_cdet_elec_12)"
    )
    parser.add_argument(
        "--keyword",
        required=True,
        help="Keyword to search for on the page (e.g., 'drone')"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=15,
        help="Interval in minutes between checks (default is 15 minutes)"
    )
    parser.add_argument(
        "--sender-email",
        required=True,
        help="Email address to send the alert from"
    )
    parser.add_argument(
        "--sender-password",
        required=True,
        help="Password for the sender email"
    )
    parser.add_argument(
        "--recipient-email",
        required=True,
        help="Email address to send the alert to"
    )
    args = parser.parse_args()

    # Verify that the URL is from woot.com
    if not re.match(r'https?://(www\.)?woot\.com', args.url):
        print("Error: URL must be from the woot.com domain.")
        sys.exit(1)

    check_interval = args.interval * 60

    print(f"Monitoring {args.url} for keyword '{args.keyword}' every {args.interval} minutes.")

    while True:
        try:
            response = requests.get(args.url)
            if response.status_code == 200:
                # Perform a case-insensitive search
                page_content = response.text.lower()
                if args.keyword.lower() in page_content:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Keyword '{args.keyword}' found on the page!")
                    subject = "Keyword Alert: Found on woot.com"
                    body = (f"The keyword '{args.keyword}' was found on the page:\n{args.url}\n"
                            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    send_email_alert(args.sender_email, args.sender_password, args.recipient_email, subject, body)
                else:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Keyword '{args.keyword}' not found.")
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to fetch page (status code: {response.status_code}).")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error occurred: {e}")
        
        time.sleep(check_interval)

if __name__ == "__main__":
    main()

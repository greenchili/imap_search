import argparse
import imaplib
import email

def search_emails(imap_server, username, password, search_text, folder_name, search_option):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)

    try:
        # Select the mailbox
        mailbox = f'"{folder_name}"'
        mail.select(mailbox)

        # Construct the search query based on the selected search option
        search_query = ''
        if search_text:
            if search_option == 'subject':
                search_query = f'SUBJECT "{search_text}"'
            elif search_option == 'sender':
                search_query = f'FROM "{search_text}"'
            elif search_option == 'content':
                search_query = f'TEXT "{search_text}"'

        # Search for emails based on the search query
        _, data = mail.search(None, search_query)

        # Get a list of email IDs
        email_ids = data[0].split()

        # Iterate over the email IDs and fetch the email information
        for email_id in email_ids:
            _, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract the subject, sender, and date from the email headers
            subject = msg['Subject']
            sender = msg['From']
            date = msg['Date']

            # Display the subject, sender, and date
            print(f"Email ID: {email_id.decode('utf-8')}")
            print(f"Subject: {subject}")
            print(f"Sender: {sender}")
            print(f"Date: {date}\n")

    except imaplib.IMAP4.error as e:
        print(f"Failed to select the folder: {e}")

    # Close the connection
    mail.close()
    mail.logout()

def main():
    parser = argparse.ArgumentParser(description="Search emails in an IMAP mailbox")
    parser.add_argument("-s", "--imap_server", required=True, help="IMAP server address")
    parser.add_argument("-u", "--username", required=True, help="Email username")
    parser.add_argument("-p", "--password", required=True, help="Email password")
    parser.add_argument("-t", "--search_text", help="Text to search in subject, sender, or content")
    parser.add_argument("-f", "--folder_name", required=True, help="Folder name to search within")

    search_options = parser.add_mutually_exclusive_group(required=True)
    search_options.add_argument("-j", "--subject", action="store_const", dest="search_option", const="subject",
                                help="Search in the subject")
    search_options.add_argument("-d", "--sender", action="store_const", dest="search_option", const="sender",
                                help="Search in the sender")
    search_options.add_argument("-c", "--content", action="store_const", dest="search_option", const="content",
                                help="Search in the content")

    args = parser.parse_args()

    search_emails(args.imap_server, args.username, args.password, args.search_text, args.folder_name, args.search_option)

if __name__ == "__main__":
    main()

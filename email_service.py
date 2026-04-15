from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

# allowing email notifications to be send using SendGrid using an API key
def send_email(opportunity_id, result, data, recipient_email):
    message = Mail(
        from_email="hectoravjr@outlook.com",
        to_emails=recipient_email,

        subject=f"Opportunity #{opportunity_id} Evaluation Result",
        
        plain_text_content=f"""

            Opportunity ID: {opportunity_id}

            Score: {result['score']}
            Decision: {result['decision']}

            Breakdown:
            {result['breakdown']}

            Data:
            {data}
        """
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        sg.send(message)
        print(f"[Email Sent] Opportunity ID: {opportunity_id}")
    except Exception as e:
        print(f"[Error] Failed to send email for Opportunity ID: {opportunity_id}. Error: {e}")

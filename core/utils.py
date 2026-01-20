from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
# import xhtml2pdf.pisa as pisa # If you want real PDF, you need reportlab or xhtml2pdf. 
# For "PDF o HTML simple", HTML is easier without extra deps. I will stick to HTML attachment or body.

def send_invoice_email(user, subscription, plan_name, amount_cents):
    subject = f"Invoice for your purchase: {plan_name}"
    
    # Simple HTML Invoice context
    context = {
        'user': user,
        'subscription': subscription,
        'plan_name': plan_name,
        'amount': amount_cents / 100,
        'date': subscription.start_date,
    }
    
    # Render HTML content
    # You would typically have a template 'emails/invoice.html'
    # html_content = render_to_string('emails/invoice.html', context)
    
    # Fallback simple string for now if template doesn't exist
    html_content = f"""
    <h1>Thank you for your purchase!</h1>
    <p>Hi {user.first_name},</p>
    <p>This is a confirmation of your subscription to <strong>{plan_name}</strong>.</p>
    <p>Amount Paid: ${amount_cents / 100:.2f}</p>
    <p>Date: {subscription.start_date}</p>
    <hr>
    <p>We are excited to have you on board!</p>
    """

    email = EmailMessage(
        subject,
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.content_subtype = "html"  # Main content is now text/html
    
    # If we wanted to attach a PDF, we would generate it here.
    # For "HTML simple como Invoice", attaching the HTML file is an option.
    
    # email.attach('invoice.html', html_content, 'text/html')
    
    try:
        email.send()
    except Exception as e:
        print(f"Error sending invoice: {e}")

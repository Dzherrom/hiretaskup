from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

def send_welcome_email(user_email, first_name):
    subject = "Welcome to TaskUp — Your assistant is being prepared"
    from_email = "hello@hiretaskup.com"
    to_emails = [user_email]

    # Contenido HTML con formato adecuado
    html_content = f"""
    <p>Hi {first_name},</p>
    
    <p>Welcome to TaskUp 👋✅ Your subscription is confirmed, and you’re officially on your way to having a dedicated assistant helping you stay organized, move faster, and get more done—without the stress.</p>
    
    <p><strong>Here’s what happens next:</strong></p>
    
    <p>✅ <strong>Step 1 — Tell us what you need (2–4 minutes)</strong><br>
    Complete this onboarding form so we can match you with the right assistant:<br>
    <a href="https://forms.gle/c4cGH6r3y33HcfqG7">https://forms.gle/c4cGH6r3y33HcfqG7</a></p>
    
    <p>✅ <strong>Step 2 — We review your needs & priorities</strong><br>
    We’ll identify your key tasks, preferred communication style, and the type of assistant that fits your workflow best.</p>
    
    <p>✅ <strong>Step 3 — Your assistant setup begins</strong><br>
    Once we have your answers, we’ll reach out to confirm next steps and get everything moving quickly.</p>
    
    <p><em>Quick note: The more detail you provide in the form, the faster we can build a smooth onboarding and deliver the best experience from day one.</em></p>
    
    <p>If you have any questions at all, simply reply to this email — we’re here and ready.</p>
    
    <p>Best regards,<br>
    TaskUp Team<br>
    <a href="mailto:hello@hiretaskup.com">hello@hiretaskup.com</a></p>
    """

    # Versión texto plano
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send()
        return True
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False

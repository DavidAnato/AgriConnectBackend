from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import random
from decouple import config

def send_password_reset_email(email, otp_code):
    """
    Envoie un email de réinitialisation de mot de passe.

    :param email: Adresse email du destinataire.
    :param otp_code: Code OTP pour la réinitialisation du mot de passe.
    """
    subject = "Password Reset Request"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Reset Request</title>
        <style>
            body {{
                background-color: #f3f4f6;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0 auto;
            }}
            .container {{
                max-width: 600px;
                padding: 20px;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: #fff;
                text-decoration: none;
                border-radius: 3px;
                margin-top: 20px;
                font-size: 1.2rem;
            }}
            .otp-code {{
                font-size: 2rem;
                font-weight: 600;
                margin-top: 1.3rem;
                color: #007bff;
                letter-spacing: 2px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">Password Reset Request</h2>
            <p>Hello,</p>
            <p>We received a request to reset your password. Your OTP code is:</p>
            <p class="otp-code">{otp_code}</p>
            <p style="margin-top: 20px; color: #666;">This code will expire in 3 hours.</p>
            <p style="margin-top: 20px;">If you did not request this, you can safely ignore this email.</p>
            <p>Regards,<br>The ConnectMe Team</p>
        </div>
    </body>
    </html>
    """
    text_content = strip_tags(html_content)
    
    try:
        email_msg = EmailMultiAlternatives(
            subject, text_content, from_email=settings.EMAIL_HOST_USER, to=[email]
        )
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()
    except Exception as e:
        raise Exception(f"Failed to send password reset email: {str(e)}")

def send_activation_email(email, otp_code):
    """
    Envoie un email d'activation de compte avec un design moderne et professionnel.
    
    :param email: Adresse email du destinataire
    :param otp_code: Code OTP pour l'activation du compte
    :raises Exception: En cas d'échec d'envoi de l'email
    """
    FRONTEND_URL = config('FRONTEND_URL', default="")
    subject = "🏊‍♀️ Activez votre compte SwimConnect"
    
    # Construction de l'URL d'activation
    activation_url = f"{FRONTEND_URL}/active-email?otp_code={otp_code}&email={email}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Activation de compte SwimConnect</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333333;
                background-color: #f8fafc;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 30px;
                text-align: center;
                color: white;
            }}
            
            .header h1 {{
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
            
            .header .subtitle {{
                font-size: 16px;
                opacity: 0.9;
                font-weight: 300;
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .welcome-text {{
                font-size: 18px;
                color: #2d3748;
                margin-bottom: 30px;
                text-align: center;
            }}
            
            .otp-section {{
                background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
                border-radius: 8px;
                padding: 30px;
                text-align: center;
                margin: 30px 0;
                border-left: 4px solid #667eea;
            }}
            
            .otp-label {{
                font-size: 14px;
                color: #718096;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            
            .otp-code {{
                font-size: 32px;
                font-weight: 700;
                color: #667eea;
                letter-spacing: 4px;
                font-family: 'Courier New', monospace;
                background-color: white;
                padding: 15px 25px;
                border-radius: 8px;
                display: inline-block;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 10px 0;
            }}
            
            .activation-button {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                padding: 15px 35px;
                border-radius: 50px;
                font-weight: 600;
                font-size: 16px;
                margin: 20px 0;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
            }}
            
            .activation-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }}
            
            .expiry-notice {{
                background-color: #fff5f5;
                border-left: 4px solid #fc8181;
                padding: 15px 20px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            
            .expiry-notice .icon {{
                display: inline-block;
                margin-right: 8px;
                font-size: 16px;
            }}
            
            .expiry-text {{
                color: #c53030;
                font-weight: 500;
                font-size: 14px;
            }}
            
            .instructions {{
                background-color: #f0fff4;
                border-left: 4px solid #48bb78;
                padding: 20px;
                margin: 25px 0;
                border-radius: 4px;
            }}
            
            .instructions h3 {{
                color: #2f855a;
                margin-bottom: 10px;
                font-size: 16px;
            }}
            
            .instructions ol {{
                color: #2d3748;
                margin-left: 20px;
            }}
            
            .instructions li {{
                margin-bottom: 8px;
                font-size: 14px;
            }}
            
            .footer {{
                background-color: #f7fafc;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            
            .footer-text {{
                color: #718096;
                font-size: 14px;
                margin-bottom: 15px;
            }}
            
            .brand {{
                color: #667eea;
                font-weight: 700;
                font-size: 16px;
            }}
            
            .support-info {{
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                color: #a0aec0;
                font-size: 12px;
            }}
            
            @media (max-width: 600px) {{
                .email-container {{
                    margin: 10px;
                }}
                
                .header, .content, .footer {{
                    padding: 25px 20px;
                }}
                
                .otp-code {{
                    font-size: 24px;
                    letter-spacing: 2px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>🏊‍♀️ SwimConnect</h1>
                <div class="subtitle">Votre plateforme de natation</div>
            </div>
            
            <div class="content">
                <div class="welcome-text">
                    <strong>Bienvenue dans la communauté SwimConnect !</strong><br>
                    Nous sommes ravis de vous accueillir parmi nous.
                </div>
                
                <div class="otp-section">
                    <div class="otp-label">Votre code d'activation</div>
                    <div class="otp-code">{otp_code}</div>
                    <p style="color: #718096; font-size: 14px; margin-top: 15px;">
                        Utilisez ce code pour activer votre compte
                    </p>
                </div>
                
                <div style="text-align: center;">
                    <a href="{activation_url}" class="activation-button">
                        ✨ Activer mon compte maintenant
                    </a>
                </div>
                
                <div class="instructions">
                    <h3>📋 Comment procéder :</h3>
                    <ol>
                        <li>Cliquez sur le bouton d'activation ci-dessus</li>
                        <li>Ou copiez-collez le code d'activation sur la page d'activation</li>
                        <li>Votre compte sera immédiatement activé</li>
                        <li>Vous pourrez alors profiter de toutes les fonctionnalités</li>
                    </ol>
                </div>
                
                <div class="expiry-notice">
                    <span class="icon">⏰</span>
                    <span class="expiry-text">
                        <strong>Important :</strong> Ce code expirera dans 3 heures pour des raisons de sécurité.
                    </span>
                </div>
            </div>
            
            <div class="footer">
                <div class="footer-text">
                    Si vous n'avez pas créé de compte, vous pouvez ignorer cet email en toute sécurité.
                </div>
                
                <div class="brand">
                    L'équipe SwimConnect 🌊
                </div>
                
                <div class="support-info">
                    Besoin d'aide ? Contactez notre support client<br>
                    Cet email a été envoyé automatiquement, merci de ne pas y répondre.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Version texte pour les clients email qui ne supportent pas le HTML
    text_content = f"""
    SwimConnect - Activation de compte
    
    Bienvenue dans la communauté SwimConnect !
    
    Votre code d'activation : {otp_code}
    
    Pour activer votre compte, rendez-vous sur :
    {activation_url}
    
    Ou utilisez le code d'activation sur la page d'activation de notre site.
    
    IMPORTANT : Ce code expirera dans 3 heures.
    
    Si vous n'avez pas créé de compte, veuillez ignorer cet email.
    
    Cordialement,
    L'équipe SwimConnect
    """
    
    try:
        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email]
        )
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()
        
    except Exception as e:
        # Log l'erreur pour le debugging (optionnel)
        raise Exception(f"Échec de l'envoi de l'email d'activation: {str(e)}")
        
def generate_otp_code():
    """
    Génère un code OTP à 6 chiffres.
    """
    return str(random.randint(100000, 999999))

def send_whatsapp_message(phone_number, otp_code):
    """
    Envoie un message WhatsApp avec le code OTP.
    Cette fonction doit être implémentée selon votre fournisseur de service.
    
    :param phone_number: Numéro de téléphone du destinataire.
    :param otp_code: Code OTP à envoyer.
    """
    # TODO: Implémenter l'envoi de message WhatsApp
    # Vous pouvez utiliser des services comme Twilio, WhatsApp Business API, etc.
    
    message = f"Your OTP code is: {otp_code}. This code will expire in 3 hours."
    
    # Exemple avec Twilio (vous devez installer twilio et configurer les credentials)
    # from twilio.rest import Client
    # 
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=message,
    #     from_=settings.TWILIO_WHATSAPP_NUMBER,
    #     to=f'whatsapp:{phone_number}'
    # )
    # return message.sid
    
    raise NotImplementedError("WhatsApp messaging not implemented yet")

def send_sms_message(phone_number, otp_code):
    """
    Envoie un SMS avec le code OTP.
    
    :param phone_number: Numéro de téléphone du destinataire.
    :param otp_code: Code OTP à envoyer.
    """
    message = f"Your OTP code is: {otp_code}. This code will expire in 3 hours."
    
    # TODO: Implémenter l'envoi de SMS
    # Exemple avec Twilio
    # from twilio.rest import Client
    # 
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=message,
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=phone_number
    # )
    # return message.sid
    
    raise NotImplementedError("SMS messaging not implemented yet")
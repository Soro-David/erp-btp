import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from app.core.config import settings


def send_invitation_email(
    to_email: str,
    invitation_link: str,
    otp_code: str,
    recipient_name: Optional[str] = None,
) -> bool:
    """
    Envoie un email d'invitation avec un code OTP à 4 chiffres et un lien d'activation sécurisé.
    Si SMTP_HOST n'est pas configuré ou en environnement de dev, affiche le code et le lien dans les logs.
    """
    display_name = recipient_name.strip() if recipient_name and recipient_name.strip() else "Cher Propriétaire / Dirigeant"

    # Message texte brut de secours
    text_content = f"""
Bonjour {display_name},

Vous avez été invité(e) en tant que Propriétaire (Owner) sur la plateforme BTP Manager - ERP Génie Civil.

Voici votre code de validation OTP à 4 chiffres :
[ {otp_code} ]

Pour configurer votre mot de passe et finaliser votre profil afin d'accéder à votre espace entreprise, veuillez cliquer sur le lien ci-dessous (valable {settings.INVITATION_TOKEN_EXPIRE_HOURS} heures) :

{invitation_link}

Renseignez le code OTP {otp_code} sur la page d'activation pour confirmer votre inscription.

Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email.

L'équipe BTP Manager
"""

    # Message HTML responsive aux couleurs de BTP Manager
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Invitation BTP Manager</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; color: #1e293b;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f1f5f9; padding: 40px 10px;">
    <tr>
      <td align="center">
        <!-- Container principal -->
        <table width="100%" max-width="600" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04); border: 1px solid #e2e8f0;">
          
          <!-- En-tête BTP Manager -->
          <tr>
            <td style="background-color: #0f294a; padding: 32px 40px; text-align: left;">
              <table border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td style="vertical-align: middle;">
                    <div style="background-color: #1d4ed8; color: #ffffff; width: 44px; height: 44px; border-radius: 12px; text-align: center; line-height: 44px; font-weight: 900; font-size: 20px; display: inline-block;">
                      🏗️
                    </div>
                  </td>
                  <td style="padding-left: 16px; vertical-align: middle;">
                    <div style="color: #ffffff; font-size: 18px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">BTP MANAGER</div>
                    <div style="color: #93c5fd; font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;">ERP GÉNIE CIVIL & CHANTIERS</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Contenu principal -->
          <tr>
            <td style="padding: 40px;">
              <h2 style="margin: 0 0 16px 0; color: #0f172a; font-size: 22px; font-weight: 700; line-height: 1.3;">
                Bienvenue sur BTP Manager !
              </h2>
              
              <p style="margin: 0 0 20px 0; color: #475569; font-size: 15px; line-height: 1.6;">
                Bonjour <strong>{display_name}</strong>,
              </p>

              <p style="margin: 0 0 24px 0; color: #475569; font-size: 15px; line-height: 1.6;">
                Un compte <strong>Propriétaire (Owner)</strong> a été préparé pour vous par l'administration centrale. Renseignez le code de validation ci-dessous et définissez votre mot de passe pour accéder à votre espace de pilotage ERP.
              </p>

              <!-- Encadré Code OTP -->
              <div style="background-color: #f0fdf4; border: 2px dashed #16a34a; border-radius: 14px; padding: 22px; text-align: center; margin-bottom: 28px;">
                <div style="font-size: 12px; font-weight: 700; color: #15803d; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;">
                  🔐 Votre code de validation OTP
                </div>
                <div style="font-size: 34px; font-weight: 900; letter-spacing: 12px; color: #14532d; font-family: monospace; margin: 6px 0;">
                  {otp_code}
                </div>
                <div style="font-size: 12px; color: #4b5563; margin-top: 6px;">
                  Ce code à 4 chiffres est requis pour valider votre compte.
                </div>
              </div>

              <!-- Encadré Rôle -->
              <div style="background-color: #f8fafc; border-left: 4px solid #1d4ed8; border-radius: 8px; padding: 14px 18px; margin-bottom: 28px;">
                <div style="font-size: 11px; font-weight: 700; color: #1d4ed8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px;">Rôle attribué</div>
                <div style="font-size: 13px; color: #0f172a; font-weight: 600;">Direction / Propriétaire d'Entreprise BTP</div>
              </div>

              <!-- Bouton d'action -->
              <table border="0" cellspacing="0" cellpadding="0" width="100%" style="margin-bottom: 28px;">
                <tr>
                  <td align="center">
                    <a href="{invitation_link}" target="_blank" style="background-color: #1d4ed8; color: #ffffff; text-decoration: none; font-size: 15px; font-weight: 700; padding: 16px 36px; border-radius: 12px; display: inline-block; box-shadow: 0 4px 14px 0 rgba(29, 78, 216, 0.39); transition: all 0.2s ease;">
                      Définir mon mot de passe & Finaliser mon profil →
                    </a>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 16px 0; color: #64748b; font-size: 13px; line-height: 1.5; text-align: center;">
                Ce lien et ce code expireront dans <strong>{settings.INVITATION_TOKEN_EXPIRE_HOURS} heures</strong>.
              </p>

              <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;" />

              <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.5;">
                Si le bouton ci-dessus ne fonctionne pas, copiez et collez l'adresse suivante directement dans votre navigateur web :<br />
                <a href="{invitation_link}" style="color: #1d4ed8; word-break: break-all;">{invitation_link}</a>
              </p>
            </td>
          </tr>

          <!-- Pied de page -->
          <tr>
            <td style="background-color: #f8fafc; padding: 24px 40px; border-top: 1px solid #e2e8f0; text-align: center;">
              <p style="margin: 0 0 6px 0; color: #64748b; font-size: 12px; font-weight: 600;">
                BTP Manager • Solution Cloud Intégrée de Gestion BTP & Génie Civil
              </p>
              <p style="margin: 0; color: #94a3b8; font-size: 11px;">
                Cet email automatique vous a été envoyé pour la sécurisation de votre accès.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    # Affichage systématique dans la console (idéal pour le développement et le debug)
    print("\n" + "=" * 76)
    print("📧 [INVITATION BTP MANAGER - EMAIL SIMULÉ EN CONSOLE]")
    print(f"👉 Destinataire     : {to_email}")
    print(f"👉 Nom / Titulaire  : {display_name}")
    print(f"🔐 CODE OTP (4 CAR) : {otp_code}")
    print(f"👉 Durée de validité: {settings.INVITATION_TOKEN_EXPIRE_HOURS} heures")
    print(f"🔗 LIEN D'ACTIVATION: {invitation_link}")
    print("=" * 76 + "\n")

    # Envoi SMTP réel si configuré
    smtp_host = settings.EFFECTIVE_SMTP_HOST
    if smtp_host:
        try:
            from_email = settings.EFFECTIVE_FROM_EMAIL
            from_name = settings.EFFECTIVE_FROM_NAME
            smtp_port = settings.EFFECTIVE_SMTP_PORT
            smtp_user = settings.EFFECTIVE_SMTP_USER
            smtp_pass = settings.EFFECTIVE_SMTP_PASSWORD

            message = MIMEMultipart("alternative")
            message["Subject"] = "Activez votre compte Propriétaire - BTP Manager"
            message["From"] = f"{from_name} <{from_email}>"
            message["To"] = to_email

            part1 = MIMEText(text_content, "plain", "utf-8")
            part2 = MIMEText(html_content, "html", "utf-8")
            message.attach(part1)
            message.attach(part2)

            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.ehlo()
                if settings.SMTP_TLS:
                    server.starttls()
                    server.ehlo()
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.sendmail(from_email, [to_email], message.as_string())

            print(f"✅ [EMAIL] Email d'invitation envoyé avec succès via SMTP ({smtp_host}:{smtp_port}) à {to_email}")
            return True
        except Exception as e:
            print(f"⚠️ [EMAIL] Erreur lors de l'envoi SMTP à {to_email} : {e}")
            return False

    return True

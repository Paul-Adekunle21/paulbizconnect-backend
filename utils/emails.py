from flask_mail import Message

def send_otp_email(mail, recipient_name, recipient_email, otp):
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background:#f0f4f8;font-family:'Segoe UI',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4f8;padding:40px 0;">
        <tr>
          <td align="center">
            <table width="560" cellpadding="0" cellspacing="0" style="background:white;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

              <!-- HEADER -->
              <tr>
                <td style="background:linear-gradient(135deg,#1a73e8 0%,#0d47a1 100%);padding:40px;text-align:center;">
                  <h1 style="margin:0;color:white;font-size:28px;font-weight:800;letter-spacing:-0.5px;">
                    PaulBiz<span style="color:#93c5fd;">Connect</span>
                  </h1>
                  <p style="margin:8px 0 0;color:rgba(255,255,255,0.75);font-size:14px;">
                    Business Connections Made Simple
                  </p>
                </td>
              </tr>

              <!-- BODY -->
              <tr>
                <td style="padding:40px;">

                  <!-- GREETING -->
                  <p style="margin:0 0 8px;font-size:22px;font-weight:700;color:#1a1a2e;">
                    Hello, {recipient_name}! 👋
                  </p>
                  <p style="margin:0 0 28px;font-size:15px;color:#555;line-height:1.6;">
                    Thank you for joining <strong>PaulBizConnect</strong>. To complete your 
                    registration, please use the verification code below:
                  </p>

                  <!-- OTP BOX -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td align="center">
                        <div style="background:linear-gradient(135deg,#e8f0fe,#dbeafe);border:2px dashed #1a73e8;border-radius:16px;padding:32px;margin-bottom:28px;display:inline-block;width:100%;box-sizing:border-box;">
                          <p style="margin:0 0 8px;font-size:13px;font-weight:600;color:#1a73e8;text-transform:uppercase;letter-spacing:2px;">
                            Your Verification Code
                          </p>
                          <p style="margin:0;font-size:52px;font-weight:900;color:#0d47a1;letter-spacing:14px;font-family:'Courier New',monospace;">
                            {otp}
                          </p>
                        </div>
                      </td>
                    </tr>
                  </table>

                  <!-- TIMER WARNING -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    <tr>
                      <td style="background:#fff8e1;border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;padding:14px 18px;">
                        <p style="margin:0;font-size:14px;color:#92400e;">
                          ⏰ <strong>This code expires in 10 minutes.</strong> Please do not share it with anyone.
                        </p>
                      </td>
                    </tr>
                  </table>

                  <!-- STEPS -->
                  <p style="margin:0 0 16px;font-size:15px;font-weight:700;color:#1a1a2e;">
                    How to verify:
                  </p>
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    <tr>
                      <td style="padding:8px 0;">
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="background:#1a73e8;color:white;width:28px;height:28px;border-radius:50%;text-align:center;font-size:13px;font-weight:700;vertical-align:middle;">1</td>
                            <td style="padding-left:12px;font-size:14px;color:#444;">Go back to the PaulBizConnect registration page</td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:8px 0;">
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="background:#1a73e8;color:white;width:28px;height:28px;border-radius:50%;text-align:center;font-size:13px;font-weight:700;vertical-align:middle;">2</td>
                            <td style="padding-left:12px;font-size:14px;color:#444;">Enter the 6-digit code shown above</td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:8px 0;">
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="background:#1a73e8;color:white;width:28px;height:28px;border-radius:50%;text-align:center;font-size:13px;font-weight:700;vertical-align:middle;">3</td>
                            <td style="padding-left:12px;font-size:14px;color:#444;">Click <strong>Verify</strong> to activate your account</td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>

                  <!-- SECURITY NOTE -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    <tr>
                      <td style="background:#fef2f2;border-left:4px solid #ef4444;border-radius:0 8px 8px 0;padding:14px 18px;">
                        <p style="margin:0;font-size:14px;color:#991b1b;">
                          🔒 <strong>Security tip:</strong> PaulBizConnect will never ask for your OTP via phone call or chat. If anyone asks, it's a scam.
                        </p>
                      </td>
                    </tr>
                  </table>

                  <!-- CLOSING -->
                  <p style="margin:0;font-size:15px;color:#555;line-height:1.6;">
                    If you did not create an account with PaulBizConnect, you can safely ignore this email.
                  </p>

                </td>
              </tr>

              <!-- FOOTER -->
              <tr>
                <td style="background:#f8fafc;border-top:1px solid #e2e8f0;padding:24px 40px;text-align:center;">
                  <p style="margin:0 0 6px;font-size:13px;font-weight:700;color:#1a73e8;">
                    PaulBizConnect
                  </p>
                  <p style="margin:0 0 6px;font-size:12px;color:#94a3b8;">
                    Connecting Businesses & Clients Seamlessly
                  </p>
                  <p style="margin:0;font-size:11px;color:#cbd5e1;">
                    © 2024 PaulBizConnect. All rights reserved.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    '''

    msg = Message(
        subject='🔐 Your PaulBizConnect Verification Code',
        recipients=[recipient_email],
        html=html
    )
    mail.send(msg)


def send_welcome_email(mail, recipient_name, recipient_email, account_type):
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background:#f0f4f8;font-family:'Segoe UI',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4f8;padding:40px 0;">
        <tr>
          <td align="center">
            <table width="560" cellpadding="0" cellspacing="0" style="background:white;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

              <!-- HEADER -->
              <tr>
                <td style="background:linear-gradient(135deg,#1a73e8 0%,#0d47a1 100%);padding:40px;text-align:center;">
                  <div style="font-size:48px;margin-bottom:12px;">🎉</div>
                  <h1 style="margin:0;color:white;font-size:28px;font-weight:800;">
                    Welcome to PaulBiz<span style="color:#93c5fd;">Connect</span>!
                  </h1>
                  <p style="margin:8px 0 0;color:rgba(255,255,255,0.75);font-size:14px;">
                    Your account is now active
                  </p>
                </td>
              </tr>

              <!-- BODY -->
              <tr>
                <td style="padding:40px;">
                  <p style="margin:0 0 20px;font-size:22px;font-weight:700;color:#1a1a2e;">
                    You're all set, {recipient_name}! 🚀
                  </p>
                  <p style="margin:0 0 28px;font-size:15px;color:#555;line-height:1.6;">
                    Your <strong>{'Business' if account_type == 'business' else 'Client'} Account</strong> 
                    has been successfully verified. Here's what you can do now:
                  </p>

                  <!-- FEATURES -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    {''.join([
                      f"""
                      <tr>
                        <td style="padding:10px 0;border-bottom:1px solid #f0f4f8;">
                          <table cellpadding="0" cellspacing="0">
                            <tr>
                              <td style="font-size:24px;width:40px;">{icon}</td>
                              <td style="padding-left:12px;">
                                <p style="margin:0;font-size:14px;font-weight:700;color:#1a1a2e;">{title}</p>
                                <p style="margin:2px 0 0;font-size:13px;color:#888;">{desc}</p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                      """
                      for icon, title, desc in [
                        ('💬', 'Real-time Messaging', 'Chat with businesses and clients instantly'),
                        ('📄', 'File Sharing', 'Share documents, invoices and files easily'),
                        ('💳', 'Payments', 'Send and receive payments securely'),
                        ('🔔', 'Notifications', 'Stay updated with real-time alerts'),
                      ]
                    ])}
                  </table>

                  <!-- CTA BUTTON -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    <tr>
                      <td align="center">
                        <a href="http://127.0.0.1:5500/index.html"
                           style="display:inline-block;background:linear-gradient(135deg,#1a73e8,#0d47a1);color:white;text-decoration:none;padding:16px 40px;border-radius:50px;font-size:15px;font-weight:700;letter-spacing:0.5px;">
                          Go to My Dashboard →
                        </a>
                      </td>
                    </tr>
                  </table>

                  <p style="margin:0;font-size:15px;color:#555;line-height:1.6;">
                    Welcome aboard! We're excited to have you on PaulBizConnect. 🎊
                  </p>
                </td>
              </tr>

              <!-- FOOTER -->
              <tr>
                <td style="background:#f8fafc;border-top:1px solid #e2e8f0;padding:24px 40px;text-align:center;">
                  <p style="margin:0 0 6px;font-size:13px;font-weight:700;color:#1a73e8;">PaulBizConnect</p>
                  <p style="margin:0 0 6px;font-size:12px;color:#94a3b8;">Connecting Businesses & Clients Seamlessly</p>
                  <p style="margin:0;font-size:11px;color:#cbd5e1;">© 2024 PaulBizConnect. All rights reserved.</p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    '''

    msg = Message(
        subject='🎉 Welcome to PaulBizConnect — Account Verified!',
        recipients=[recipient_email],
        html=html
    )
    mail.send(msg)


def send_password_reset_email(mail, recipient_name, recipient_email, otp):
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background:#f0f4f8;font-family:'Segoe UI',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4f8;padding:40px 0;">
        <tr>
          <td align="center">
            <table width="560" cellpadding="0" cellspacing="0" style="background:white;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

              <!-- HEADER -->
              <tr>
                <td style="background:linear-gradient(135deg,#dc2626 0%,#991b1b 100%);padding:40px;text-align:center;">
                  <div style="font-size:48px;margin-bottom:12px;">🔑</div>
                  <h1 style="margin:0;color:white;font-size:26px;font-weight:800;">
                    Password Reset Request
                  </h1>
                  <p style="margin:8px 0 0;color:rgba(255,255,255,0.75);font-size:14px;">
                    PaulBizConnect Security
                  </p>
                </td>
              </tr>

              <!-- BODY -->
              <tr>
                <td style="padding:40px;">
                  <p style="margin:0 0 8px;font-size:20px;font-weight:700;color:#1a1a2e;">
                    Hi {recipient_name},
                  </p>
                  <p style="margin:0 0 28px;font-size:15px;color:#555;line-height:1.6;">
                    We received a request to reset your password. Use the code below to proceed:
                  </p>

                  <!-- OTP BOX -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td align="center">
                        <div style="background:linear-gradient(135deg,#fef2f2,#fee2e2);border:2px dashed #dc2626;border-radius:16px;padding:32px;margin-bottom:28px;width:100%;box-sizing:border-box;">
                          <p style="margin:0 0 8px;font-size:13px;font-weight:600;color:#dc2626;text-transform:uppercase;letter-spacing:2px;">
                            Password Reset Code
                          </p>
                          <p style="margin:0;font-size:52px;font-weight:900;color:#991b1b;letter-spacing:14px;font-family:'Courier New',monospace;">
                            {otp}
                          </p>
                        </div>
                      </td>
                    </tr>
                  </table>

                  <!-- WARNING -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    <tr>
                      <td style="background:#fff8e1;border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;padding:14px 18px;">
                        <p style="margin:0;font-size:14px;color:#92400e;">
                          ⏰ <strong>This code expires in 15 minutes.</strong>
                        </p>
                      </td>
                    </tr>
                  </table>

                  <!-- SECURITY NOTE -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    <tr>
                      <td style="background:#fef2f2;border-left:4px solid #ef4444;border-radius:0 8px 8px 0;padding:14px 18px;">
                        <p style="margin:0;font-size:14px;color:#991b1b;">
                          🔒 <strong>Did not request this?</strong> Your account may be at risk. 
                          Please contact us immediately and change your password.
                        </p>
                      </td>
                    </tr>
                  </table>

                  <p style="margin:0;font-size:15px;color:#555;line-height:1.6;">
                    If you did not request a password reset, please ignore this email. Your password will remain unchanged.
                  </p>
                </td>
              </tr>

              <!-- FOOTER -->
              <tr>
                <td style="background:#f8fafc;border-top:1px solid #e2e8f0;padding:24px 40px;text-align:center;">
                  <p style="margin:0 0 6px;font-size:13px;font-weight:700;color:#1a73e8;">PaulBizConnect</p>
                  <p style="margin:0 0 6px;font-size:12px;color:#94a3b8;">Connecting Businesses & Clients Seamlessly</p>
                  <p style="margin:0;font-size:11px;color:#cbd5e1;">© 2024 PaulBizConnect. All rights reserved.</p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    '''

    msg = Message(
        subject='🔑 PaulBizConnect — Password Reset Code',
        recipients=[recipient_email],
        html=html
    )
    mail.send(msg)
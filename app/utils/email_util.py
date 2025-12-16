import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
import json

class EmailUtil:
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None):
        """
        Initialize email utility. Can load config from environment variables or config file.
        
        Args:
            smtp_server: SMTP server address (default: Gmail)
            smtp_port: SMTP port (default: 587 for TLS)
            username: Email username
            password: Email password or app password
        """
        # Try to load from config file first
        config = self._load_email_config()
        
        self.smtp_server = smtp_server or config.get('smtp_server') or os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or config.get('smtp_port') or int(os.getenv('EMAIL_SMTP_PORT', '587'))
        self.username = username or config.get('email_username') or os.getenv('EMAIL_USERNAME', 'jeiboxgmr@gmail.com')
        self.password = password or config.get('email_password') or os.getenv('EMAIL_PASSWORD', 'kzpf vdzl zbrc axjf')
        
        # Load recipient list
        self.recipients = config.get('recipients', []) or self._load_recipients_from_env()
        
        logging.info(f"EmailUtil initialized with server: {self.smtp_server}:{self.smtp_port}")
    
    def _load_email_config(self):
        """Load email configuration from JSON file."""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'email_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    logging.info(f"Loaded email configuration from {config_path}")
                    return config
        except Exception as e:
            logging.warning(f"Could not load email config from file: {e}")
        
        return {}
    
    def _load_recipients_from_env(self):
        """Load recipients from environment variable."""
        recipients_str = os.getenv('EMAIL_RECIPIENTS', 'santiagovl0308@gmail.com')
        return [email.strip() for email in recipients_str.split(',')]
        
    def send_email(self, to_address, subject, body):
        """
        Send email to a single recipient.
        
        Args:
            to_address: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            
        Returns:
            dict with success status and message
        """
        try:
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_address
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to the server and send the email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Email sent successfully to {to_address}")
            return {'success': True, 'message': f'Email sent successfully to {to_address}'}
        
        except Exception as e:
            logging.error(f"Failed to send email to {to_address}: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_email_to_multiple(self, recipients, subject, body):
        """
        Send email to multiple recipients.
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            body: Email body (plain text)
            
        Returns:
            dict with overall success status and individual results
        """
        results = []
        success_count = 0
        
        for recipient in recipients:
            result = self.send_email(recipient, subject, body)
            results.append({
                'recipient': recipient,
                'success': result['success'],
                'message': result.get('message') or result.get('error')
            })
            if result['success']:
                success_count += 1
        
        return {
            'success': success_count > 0,
            'total_sent': success_count,
            'total_failed': len(recipients) - success_count,
            'results': results
        }
    
    def send_fire_alert_email(self, fire_detected, detection_results, camera_url, alert_id):
        """
        Send fire alert email to configured recipients.
        
        Args:
            fire_detected: Boolean indicating if fire was detected
            detection_results: Dict with detection details
            camera_url: URL of the camera
            alert_id: Database alert ID
            
        Returns:
            dict with email sending results
        """
        if fire_detected:
            subject = "🔥 FIRE ALERT - Fire Detected by IoT System!"
            body = self._create_fire_detected_email_body(detection_results, camera_url, alert_id)
        else:
            subject = "✓ Fire Check Complete - No Fire Detected"
            body = self._create_no_fire_email_body(detection_results, camera_url, alert_id)
        
        # Send to all configured recipients
        recipients = self.recipients if self.recipients else ['santiagovl0308@gmail.com']
        
        logging.info(f"Sending fire alert email to: {', '.join(recipients)}")
        return self.send_email_to_multiple(recipients, subject, body)
    
    def _create_fire_detected_email_body(self, detection_results, camera_url, alert_id):
        """Create email body for fire detection alert."""
        confidence = detection_results.get('confidence', 0.0)
        fire_percentage = detection_results.get('fire_percentage', 0.0)
        total_frames = detection_results.get('total_frames', 0)
        frames_with_fire = detection_results.get('frames_with_fire', 0)
        video_duration = detection_results.get('video_duration', 0)
        
        body = f"""
🚨 FIRE ALERT - IMMEDIATE ACTION REQUIRED 🚨

This is an automated alert from your IoT Fire Detection System.

FIRE HAS BEEN DETECTED in the monitored area!

═══════════════════════════════════════════════════════════
DETECTION DETAILS
═══════════════════════════════════════════════════════════

Camera Location:    {camera_url}
Alert ID:          {alert_id}
Detection Time:     {detection_results.get('analysis_timestamp', 'N/A')}

Fire Confidence:    {confidence:.1%}
Fire Coverage:      {fire_percentage:.1f}% of frames
Video Duration:     {video_duration:.1f} seconds
Total Frames:       {total_frames}
Frames with Fire:   {frames_with_fire}

═══════════════════════════════════════════════════════════
RECOMMENDED ACTIONS
═══════════════════════════════════════════════════════════

1. ⚠️  EVACUATE the area immediately if safe to do so
2. 📞 CALL emergency services (911 or local fire department)
3. 🔍 VERIFY the alert by checking the camera feed manually
4. 🚪 CLOSE doors and windows to contain the fire
5. 🧯 Use fire extinguisher ONLY if fire is small and contained
6. ⛔ DO NOT attempt to fight large fires

═══════════════════════════════════════════════════════════
SYSTEM INFORMATION
═══════════════════════════════════════════════════════════

Detection Method:   AI-powered fire detection with color analysis
System Status:      ACTIVE
Camera URL:         {camera_url}

For support or to report false alarms, please contact your system administrator.

═══════════════════════════════════════════════════════════

This is an automated message. Please do not reply to this email.
Stay safe!

IoT Fire Detection System
"""
        return body
    
    def _create_no_fire_email_body(self, detection_results, camera_url, alert_id):
        """Create email body for no fire detected notification."""
        total_frames = detection_results.get('total_frames', 0)
        video_duration = detection_results.get('video_duration', 0)
        
        body = f"""
✓ Fire Detection Check Complete - No Fire Detected

This is a notification from your IoT Fire Detection System.

A fire detection check was performed due to critical sensor readings 
(low humidity + high temperature), but no fire was detected in the 
camera footage.

═══════════════════════════════════════════════════════════
CHECK DETAILS
═══════════════════════════════════════════════════════════

Camera Location:    {camera_url}
Alert ID:          {alert_id}
Check Time:        {detection_results.get('analysis_timestamp', 'N/A')}

Result:            ✓ NO FIRE DETECTED
Video Duration:    {video_duration:.1f} seconds
Frames Analyzed:   {total_frames}

═══════════════════════════════════════════════════════════
RECOMMENDATION
═══════════════════════════════════════════════════════════

While no fire was detected, the environmental conditions (low humidity 
and high temperature) still indicate an elevated fire risk.

Please:
- Monitor the area closely
- Ensure no heat sources are left unattended
- Maintain adequate humidity levels if possible
- Keep flammable materials away from heat sources

═══════════════════════════════════════════════════════════

This is an automated message. Please do not reply to this email.

IoT Fire Detection System
"""
        return body

        
class FireAlert:
    def __init__(self, db_connection):
        self.db = db_connection
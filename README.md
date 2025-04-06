# Site-Keyword-Alert

### Setup and Usage

1. **Install Dependencies:**  
   Open a command prompt and install the required library:
   ```bash
   pip install requests
   ```

2. **Gmail Configuration:**  
   - If you’re using Gmail, you may need to enable “Less secure apps” or, preferably, create an app password if you have two-factor authentication enabled.
   - For other email providers, update the SMTP server address and port accordingly.

3. **Run the Script:**  
   Save the script (e.g., as `monitor_email.py`) and run it with the required arguments. For example:
   ```bash
   python monitor_email.py --url "https://www.woot.com/category/electronics/other-electronics?ref=w_cnt_cdet_elec_12" --keyword "drone" --sender-email "your_email@gmail.com" --sender-password "your_password" --recipient-email "recipient_email@example.com"
   ```
   
4. **Adjust as Needed:**  
   You can modify the check interval by changing the `--interval` argument (value is in minutes). This script will continuously check the provided URL and send an email alert whenever the specified keyword is found.

Due to Gmail disabling access via password, create one using "App passwords"
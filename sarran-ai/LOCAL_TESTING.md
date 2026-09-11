# Test the Sarran AI Connect page locally

## Start the website

1. Extract the project ZIP.
2. Open PowerShell inside the extracted `sarran-ai` folder.
3. Run:

   ```powershell
   python -m http.server 8000
   ```

4. Open this address in your browser:

   `http://localhost:8000/connect.html`

Keep the PowerShell window open while you test.

## What to test

1. Confirm the **Connection established** introduction appears and clears automatically. Reload and test **Skip intro**.
2. Select each of the four business challenges.
3. Confirm the workflow, recommendation, and service link change to match each selection.
4. During a workflow, test **Skip animation**, then test **Replay**.
5. Move the weekly-hours slider and confirm the annual hours and workday estimate update.
6. Select **Request My Assessment** and confirm the form opens.
7. Use **Back** and **Continue** to move through the form. You do not need to submit it.
8. Select **Save Robert’s Contact** and confirm the contact card downloads.
9. Check the call, email, LinkedIn, service, privacy, and full website links.
10. Make the browser narrow like a phone and confirm nothing is cut off.

## Reduced-motion check

In Windows, turn on **Accessibility → Visual effects → Animation effects: Off**, reload the page, and confirm the introduction and workflow display their finished state without waiting for animation.

## Test on your phone before deployment

1. Keep the computer and phone on the same Wi-Fi network.
2. In PowerShell, run `ipconfig` and find the computer’s IPv4 Address.
3. On the phone, open `http://YOUR-IP-ADDRESS:8000/connect.html`.

Windows may ask whether Python can communicate through the firewall. Allow it only on your private home or office network.

## About the finished QR code

The supplied QR code points to:

`https://www.sarranai.com/connect`

That address will begin showing the Connect page after the approved project is deployed to Vercel. Until then, scanning the production QR may show a not-found page. The QR code does not need to be regenerated after deployment.

## Stop the local website

Return to PowerShell and press `Ctrl+C`.

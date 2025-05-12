# pyvenDF/templates/views.py

def welcome_view():
    """Render the welcome page."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WELCOME to Pyven</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f0f8ff;
                color: #333;
                text-align: center;
                padding: 50px;
                margin: 0;
            }

            h1 {
                font-size: 48px;
                font-weight: bold;
                color: #2e8b57;
                animation: fadeIn 2s ease-in-out;
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }

            p {
                font-size: 20px;
                color: #555;
            }

            .container {
                background-color: #fff;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                display: inline-block;
                margin-top: 50px;
            }

            .button {
                background-color: #2e8b57;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 20px;
                text-decoration: none;
            }

            .button:hover {
                background-color: #4caf50;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>WELCOME to Pyven</h1>
            <p>Your journey with Pyven starts here!</p>
            <a href="/" class="button">Go to Home</a>
        </div>

    </body>
    </html>
    """
    return html_content

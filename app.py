from flask import Flask, render_template, request

app = Flask(__name__)

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - ascii_base + shift) % 26
            result += chr(shifted + ascii_base)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def crack(text):
    possibilities = []
    for shift in range(26):
        decrypted = decrypt(text, shift)
        possibilities.append((shift, decrypted))
    return possibilities

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        message = request.form.get("message", "").strip()
        shift = int(request.form.get("shift", 0))

        if action == "encrypt":
            result = encrypt(message, shift)
            output = f"Encrypted message: {result}"

        elif action == "decrypt":
            result = decrypt(message, shift)
            output = f"Decrypted message: {result}"

        elif action == "crack":
            possibilities = crack(message)
            output = "All possible decryptions:<br>" + "<br>".join([f"Shift {shift}: {text}" for shift, text in possibilities])

        return render_template("index.html", output=output)

    return render_template("index.html", output="")

if __name__ == "__main__":
    app.run(debug=True)

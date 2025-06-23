## Arcade knoppen koppelen aan de website (Raspberry Pi)

1. **Benodigdheden:**
   - Raspberry Pi 5
   - 3 arcade knoppen aangesloten op GPIO 17, 27 en 22
   - Python 3
   - gpiozero (`pip install gpiozero`)
   - Flask (`pip install flask`)

2. **Python-script voor de Pi:**

```python
from flask import Flask, jsonify
from gpiozero import Button

app = Flask(__name__)

button1 = Button(17)
button2 = Button(27)
button3 = Button(22)

last_pressed = None

def check_buttons():
    global last_pressed
    if button1.is_pressed:
        last_pressed = 'video1'
    elif button2.is_pressed:
        last_pressed = 'video2'
    elif button3.is_pressed:
        last_pressed = 'video3'
    else:
        last_pressed = None

@app.route('/button')
def button():
    check_buttons()
    return jsonify({'button': last_pressed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

3. **Start het script op de Pi:**
   - Sla het script op als `arcade_buttons.py`.
   - Voer uit met: `python3 arcade_buttons.py`

4. **Pas het IP-adres aan in `assets/script.js`:**
   - Zoek naar `http://<IP-van-je-pi>:5000/button` en vervang `<IP-van-je-pi>` door het lokale IP-adres van je Raspberry Pi.

5. **Open de website in de browser op dezelfde computer of een apparaat in hetzelfde netwerk.**

Nu kun je met de arcade knoppen de animaties op de website bedienen! 
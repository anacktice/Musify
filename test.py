import pywhatkit
x = (str(pywhatkit.playonyt(topic="tracing that dream", use_api=False)).split("""\\"""))[0]
print(x)
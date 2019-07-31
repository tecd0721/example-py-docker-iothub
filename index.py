from flask import Flask, render_template
import json
import paho.mqtt.client as mqtt
import os


app = Flask(__name__)

# port from cloud environment variable or localhost:3000
port = int(os.getenv("PORT", 3000))


@app.route('/', methods=['GET'])
def root():

    if(port == 3000):
        return 'hello world! i am in the local'
    elif(port == int(os.getenv("PORT"))):
        return render_template('index.html')


vcap_services = os.getenv('VCAP_SERVICES')
vcap_services_js = json.loads(vcap_services)
service_name = 'p-rabbitmq'
broker = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['host']
username = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['username'].strip()
password = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['password'].strip()
mqtt_port = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['port']


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/hello")
    print('subscribe on /hello')


def on_message(client, userdata, msg):
    print(msg.topic+','+msg.payload.decode())

client = mqtt.Client()

client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, mqtt_port, 60)

client.loop_start()


if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)


from pywebio.input import input,select
from pywebio.input import textarea
from pywebio.output import put_text, put_image, put_html,put_code
import redis
import secrets
from flask import  Flask
from pywebio.platform.flask import webio_view
import argparse
from pywebio import start_server
from pywebio.input import input

app=Flask(__name__)
# Connect to the Redis server
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# Define a Redis key for storing the data-to-code mapping
REDIS_MAPPING_KEY = "data_to_code_mapping"

# Load the data-to-code mapping from Redis
data_to_code = {code.decode('utf-8'): data.decode('utf-8') for code, data in redis_client.hgetall(REDIS_MAPPING_KEY).items()}

def save_mapping_to_redis():
    # Save the data-to-code mapping to Redis
    for code, data in data_to_code.items():
        redis_client.hset(REDIS_MAPPING_KEY, code, data)

def generate_code(data):
    # Generate a random code and store the data-to-code mapping
    code = secrets.token_hex(4)  # Generate an 8-character hexadecimal code
    data_to_code[code] = data
    save_mapping_to_redis()
    return code

def insert_data():
    # Input form to insert data and generate a code
    #data = input("Enter your Secret:", type=textarea)
    data = textarea("Enter your Secret✨:", rows=5, placeholder="Dont share your secrets......",required=True)

    code = generate_code(data)
    put_text(f"Secret inserted successfully. Your secret code is:")
    larger_text = f'<span style="font-size: 70px;">{code}</span>'
    put_html(larger_text)





    
def retrieve_data():
    # Input form to retrieve data using a code
    code = input("Enter the secret code to retrieve you  data:", type='text')
    data = data_to_code.get(code)
    if data:
        put_text("Secret retrieved Successfully:")

        put_text(data) 
        


    else:
        put_text("Invalid code. Secret not found.")

def home():

    put_html(r"""<h1  align="center"><strong> SECRET KEEPER ☁️ </strong></h1>""")
    img = open('logo.png', 'rb').read() 
    put_image(img, width='100px')  # size of image

    put_code("Secret Keeper is an online webapp to create and share secrets.",
             'python')


    option=select('Select an Option!', ['Insert Secret', 'Retrieve Secret'])
    if option == 'Insert Secret':
            insert_data()
    elif option == 'Retrieve Secret':
                retrieve_data()


# To allow reloading of web browser and mentioning the port
app.add_url_rule('/home', 'webio_view', webio_view(home), methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8083)
    args = parser.parse_args()



    start_server(home, port=args.port,debug=True)

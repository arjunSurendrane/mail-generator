
from pymongo import MongoClient

uri = "mongodb+srv://mainUser:HQ9sxIPMAw7u5Le8@cluster0.fhv4gas.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['mailGenerator']
collection = db['user']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
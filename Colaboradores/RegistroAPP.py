from app.AWSConnections import AWSConnections

aws = AWSConnections()
awsSession = aws.getSession()

def saveUserDynamoDB(session, user):
  dynamodb = session.resource('dynamodb')
  table = dynamodb.Table('Users')
  response = table.put_item(Item=user)
  return response

print("Bienvenido a tu proceso de registro!")
user = input("Escribe tu correo electronico: ")
balance = 5000
print(f"Gracias por tu registro {user}!, iniciaras con un saldo inicial de Q{balance} \n Gracias por preferirnos")
saveUserDynamoDB(awsSession, {"balance": balance, "User": user})
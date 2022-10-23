import PySimpleGUI as sg

#dictionary contains both username and coded password. If a coded password is entered, 
#it gives the company time to shut down since that means that information has been compromised. 
#For this example, I will use a variation of the Vigenere Cypher but any type of cypher could be used in its place.

personalTheme = {
  'BACKGROUND': 'white',
  'TEXT': 'black',
  'INPUT': 'white',
  'TEXT_INPUT': 'black',
  'SCROLL': '#A2AFA6',
  'BUTTON': ('black', 'white'),
  'PROGRESS': ('#01826B', '#D0D0D0'),
  'BORDER': 1,
  'SLIDER_DEPTH': 0,
  'PROGRESS_DEPTH': 0
}

sg.theme_add_new('NewTheme', personalTheme)
sg.theme('NewTheme')

def encrypt(toCode, key):
  ans = ""
  toCode = list(toCode)
  #make key same size
  key = list(findKey(toCode, key))
  ansNum = 0
  for i in range(len(toCode)):
    if (ord(toCode[i]) < 123 and ord(toCode[i]) > 32):
      ansNum = (ord(toCode[i]) - 33) - (ord(key[i]) - 33)
      if (ansNum < 0):
        ansNum += 90
      if (ansNum < 0):
        ansNum += 90
      ans += chr(ansNum + 33)
  return ans


def decrypt(toDec, key):
  ans = ""
  toDec = list(toDec)
  #make key same size
  key = list(findKey(toDec, key))
  ansNum = 0
  for i in range(len(toDec)):
    if (ord(toDec[i]) < 123 and ord(toDec[i]) > 32):
      ansNum = ord(toDec[i]) - 33 + ord(key[i]) - 33
      ansNum = ansNum % 90
      ans += chr(ansNum + 33)
  return ans


def findKey(other, key):
  if (len(key) == len(other)):
    return key
  elif (len(key) > len(other)):
    return key[0:len(other)]
  else:
    return findKey(other, (key + key))

thisdict = {}

useInput = input("What is your Username? ")
passInput = input("What is your Password? ")

thisdict[useInput] = encrypt(useInput, passInput)
print("Your user name is " + useInput)
print("Your password is " + passInput)
print("Your password is saved as " + thisdict[useInput])


def checkPass(user, passw):
  if (user in thisdict):
    if (decrypt(thisdict[user], passw) == user):
      return True
    if (thisdict[user] == passw):
      print(
        "Internal Note : Error, coded password entered, saved information may be compromised!"
      )
  return False


layout = [[sg.Text('Login')],
          [sg.Text('Username', auto_size_text=True),
           sg.InputText()],
          [sg.Text('Password', auto_size_text=True),
           sg.InputText()], [sg.Button('Read'), sg.Exit()]]

window = sg.Window('Window that stays open',
                   layout,
                   auto_size_text=True,
                   auto_size_buttons=True)

while True:  # The Event Loop
  event, values = window.read()

  username = (values[0])
  password = (values[1])

  if (event == 'Read'):
    if (checkPass(username, password)):
      print("Password accepted, welcome!")
    else:
      print("Sorry, password or username not recognized.")
    break
  if event == sg.WIN_CLOSED or event == 'Exit':
    break

window.close()

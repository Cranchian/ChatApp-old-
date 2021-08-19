from client import Client
import time
from threading import Thread


c1 = Client(input()) # change to a str name for auto testing

c2 = Client("Mr. B")


# storing messages for UI so that messages are not gone when user quits
def update_messages():
    """
    updates the local messages list
    :return:None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # Update every 0.1 sec
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local msg list

        # display new messages
        for msg in new_messages:
            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

# input testing
while True:
    msg = input()
    if msg == "quit":
        c1.disconnect()
        break
    c1.send_message(msg)
    time.sleep(0.5)


## auto testing
# c1.send_message("hello")
# time.sleep(1)
# c2.send_message("What's up matey")
# time.sleep(1)
# c1.send_message("I can say anythin crazy")
# time.sleep(1)
# c2.send_message("whut?")
# time.sleep(1)
# c1.send_message("2323523532")
# time.sleep(1)
# c2.send_message("I guess imma sleep now")
# time.sleep(1)
#
# c2.disconnect()
# time.sleep(1)
# c1.send_message("alright bye")
# time.sleep(1)
#
# c1.disconnect()

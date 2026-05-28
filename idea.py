def processing_open():
      return 1

def processing_closed():
      pass

status = "open"

query = processing_open() if status == "open" else processing_closed()

print(query)
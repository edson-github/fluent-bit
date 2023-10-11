import monkey

with open('/tmp/index.html', 'w') as f:
    f.write("<html><body><h2>Hello Monkey</h2></body></html>")
monkey.init(None, 0, 0, '/tmp/')
monkey.configure(indexfile='index.html')

monkey.start()
raw_input("Press enter to stop the server...")
monkey.stop()

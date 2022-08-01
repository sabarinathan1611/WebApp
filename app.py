from distutils.log import debug
from views import create_app

app = create_app()




   

    
if __name__ == '__main__':
    app.run(debug=True,port=5000)
    # socketio.run(app,debug=True)
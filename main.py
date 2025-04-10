from website import create_app 

app = create_app()

#runs webserver if this file is run directly
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

    
    
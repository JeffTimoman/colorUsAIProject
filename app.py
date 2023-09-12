from webdata import app

if __name__ == '__main__':
    with app.app_context():
        #app.run(debug=True)
	    app.run(debug=False, host='10.68.103.190', port=80)

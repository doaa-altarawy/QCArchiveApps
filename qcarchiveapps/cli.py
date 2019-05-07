from .index import app

def main(args=None):
    app.run_server(debug=True)

if __name__ == '__main__':
    main()

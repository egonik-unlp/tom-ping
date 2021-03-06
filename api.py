from flask import request, Flask, url_for, redirect, render_template
import main
import os
import test
import notification
from flask_restful import Resource, Api
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import getter
app = Flask(__name__)
api = Api(app)

class Query(Resource):
    def get(self):
        return getter.consulta(), 200


class Test(Resource):
    def get(self):
        return test.main(), 200

class Test_msj(Resource):
    def get(self):
        return notification.test('chupame bien la verga tom'), 200
        



def sensor():
    # _=notification.test('chupame bien la verga tom pero periodicamente')
    main.main()
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=15)
sched.start()




# Create routes
api.add_resource(Query, '/query')
api.add_resource(Test, '/test')
api.add_resource(Test_msj, '/test_msj')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
@app.route('/')
def home():
    return render_template('view.html', tables=[getter.consulta().to_html(classes='cripto')] , titles=['las kripto eee'])
@app.route('/ultima_notificacion')
def ultima_notificacion():
    with open('falopa.html') as file:
        retv=file.read()
    return retv


# Run the application
if __name__ == '__main__':
    port= int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



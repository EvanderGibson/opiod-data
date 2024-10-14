from flask import Flask, url_for, render_template, request
from markupsafe import Markup

import os
import json
app = Flask(__name__)
    
@app.route('/')
def home():
    return render_template('about.html')
if __name__=="__main__":
    app.run(debug=True)
    
    
    
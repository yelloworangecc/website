import os,io,re

from flask import Blueprint,abort,request,render_template,current_app
from werkzeug.utils import secure_filename
from py.VideoManager import VideoSerial

module_video = Blueprint('module_video', __name__, url_prefix='/video')
current_app.config['VIDEO_SERIAL_PER_PAGE'] = 5

@module_video.route('/index')
def index():
    if not VideoSerial.load():
        return '<h1>load video serials failed</h1>'

    videoSerials = VideoSerial.getPageList(0, current_app.config['VIDEO_SERIAL_PER_PAGE'])
    return render_template('listpage.html',view_func='module_video.video',itemList=videoSerials)

# play a video from target video serial
@module_video.route('/<name>/<subname>')
def video(name,subname):
    serial = VideoSerial.get(name)
    if not video:
        return abort(404)
    return render_template('video.html',serial=serial,episodename=subname)

# create a new video serial, also provide a create page
@module_video.route('/videoserial',methods=['GET','POST'])
def videoserial(serialname):
    if request.method == 'POST':
        return 'OK'
    return '''
    <!doctype html>
    <title>Create A New Video Serial</title>
    <h1>Create A New Video Serial</h1>
    <form method=post enctype=multipart/form-data>
      <span>Serial Name</span>
      <input type=text name=serialname>
      <span>Description</span>
      <input type=text name=description>
      <input type=submit value=Submit>
    </form>
    '''

# publish a new video to serial
@module_video.route('/publish/<serialname>', methods=['GET', 'POST'])
def publish(serialname):
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'FAIL'
        
        file = request.files['file']
        filename = secure_filename(file.filename)

        content = file.read()
        with open(os.path.join(current_app.root_path, 'video', filename),'wb') as fp:
            fp.write(content)
            
        VideoSerial.add(serialname,filename,abstract)                
        return 'OK'
    return '''
    <!doctype html>
    <title>Upload Video</title>
    <h1>Upload Video</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# for upload and access hls playlist and segments
@module_video.route('/live/<filename>', methods=['GET','PUT'])
def uploaded_file(filename):
    if request.method == 'PUT':
        # Record IP
        app.config['IP'] = request.remote_addr
        # Delete file
        dot_index = filename.find('.')
        postfix = filename[dot_index+1:]
        if postfix == 'ts':
            number = int(filename[8:dot_index])
            if number >= app.config['TS_NUMBER']:
                deletefile = 'playlist'+str(number - app.config['TS_NUMBER'])+'.ts'
                deletepath = os.path.join(app.config['LIVE_FOLD'],deletefile)
                os.remove(deletepath)
                
        filepath = os.path.join(app.config['LIVE_FOLD'],filename)
        with open(filepath,mode='wb') as file:
            file.write(request.data)
        return 'success'
    else:
        return send_from_directory(app.config['LIVE_FOLD'],filename)

# for delete old segment
@module_video.route('/live/<filename>', methods=['DELETE'])
def delete_segment(filename):
    pass
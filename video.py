import os,io,re,time

from flask import Blueprint,abort,request,render_template,current_app,send_from_directory
from werkzeug.utils import secure_filename
from py.VideoManager import VideoSerial

module_video = Blueprint('module_video', __name__, url_prefix='/video')
current_app.config['LIVE_FOLD'] = 'video/live/'
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
    if not serial:
        # serial not found
        return abort(404)

    if name != 'live' and subname == 'None':
        if 'episode' not in serial.j or len(serial.j['episode']) == 0:
            # episode not found
            return abort(404)
        else:
            # get default episode
            subname = serial.j['episode'][0]
        
    return render_template('video.html',serial=serial,episode=subname)

# create a new video serial, also provide a create page
@module_video.route('/serial',methods=['POST'])
def videoserial():
    # check token 
    try:
        token=request.args["token"].encode()
        data = current_app.config['FERNET'].decrypt(token,ttl=100)
        # print(data)
        if current_app.secret_key.encode() != data:
            return abort(403)
    except:
        return abort(403)

    # check args
    f = request.args['file']
    name = request.args['name']
    description = request.args['description']
    if not name or not description:
        return abort(406)

    # create directory
    directory = os.path.join(current_app.root_path, 'video', f)
    if not os.path.exists(directory):
        os.mkdir(directory)

    # check serial & add serial
    if not VideoSerial.get(f):
        VideoSerial.add(f, name, description)
    return 'OK'

# publish a video to serial
@module_video.route('/publish/<serialname>', methods=['POST'])
def publish(serialname):
    # check token 
    # print(request.args)
    try:
        token=request.args['token'].encode()
        data = current_app.config['FERNET'].decrypt(token,ttl=100)
        if current_app.secret_key.encode() != data:
            return abort(403)
    except:
        print('decrypt failed')
        return abort(403)

    # check file
    if 'file' not in request.files:
        return abort(406)
    file = request.files['file']
    filename = secure_filename(file.filename)
    nameOnly = filename.rsplit('.', 1)[0].lower()
    
    # check serial & add episode
    serial = VideoSerial.get(serialname)
    if not serial:
        return abort(412)
    if not serial.addEpisode(nameOnly):
        return abort(404)

    # save file
    directory = os.path.join(current_app.root_path, 'video', serialname, nameOnly)
    if not os.path.exists(directory):
        os.mkdir(directory)
    filepath = os.path.join(directory, filename)
    file.save(filepath)

    os.system('ffmpeg -i {0} -vcodec copy -acodec copy -f segment -segment_list {1}/playlist.m3u8 -segment_time 10 {1}/%d.ts'.format(filepath,directory))
    time.sleep(1) # make sure the m3u8 updated 
    return 'OK'

# get playlist and ts files for a serial
@module_video.route('/<serialname>/<filename>/<ts>')
def ts(serialname,filename,ts):
    return send_from_directory(os.path.join(current_app.root_path, 'video', serialname, filename),ts)

# for upload and access live playlist and segments
@module_video.route('/live/<filename>', methods=['GET','PUT'])
def uploaded_file(filename):
    if request.method == 'PUT':
        if filename.find('.m3u8') > 0:
            # record ip
            current_app.config['IP'] = request.remote_addr
            
            # check token
            try:
                token=request.args['token'].encode()
                data = current_app.config['FERNET'].decrypt(token,ttl=100)
                if current_app.secret_key.encode() != data:
                    return abort(403)
            except:
                print('decrypt failed')
                return abort(403)
    
        # save files
        directory = current_app.config['LIVE_FOLD']
        filepath = os.path.join(directory,filename)
        if not os.path.exists(directory):
            os.mkdir(directory)
        with open(filepath,mode='wb') as file:
            file.write(request.data)
        return 'success'
    else:
        if filename == 'None':
            serial = VideoSerial.get('live')
            return render_template('video.html',serial=serial,episode='None')
        else:
            return send_from_directory(current_app.config['LIVE_FOLD'],filename)

# for delete old segment
@module_video.route('/<filename>', methods=['DELETE'])
def delete_segment(filename):
    slash_index = filename.find('\\')
    truename = filename[slash_index+1:]
    filepath = os.path.join(current_app.config['LIVE_FOLD'],truename)
    if not os.path.exists(filepath):
        os.remove(filepath)
    return 'success'

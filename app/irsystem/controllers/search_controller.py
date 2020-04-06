from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Spotify Buddy Playlist Generation"
net_id = "Matthew Simon: mls498, Grayson Campbell: gac88, Daniel Hayon: dh488, Theo Carrel: tjc233, Carol Zhang: cz233"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)




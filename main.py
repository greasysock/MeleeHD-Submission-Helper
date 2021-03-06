import os, shutil,dropbox, time, platform, json, tempfile,zipfile
from splinter import Browser
from support import ffhelper, da, template
from collections import defaultdict

db_token = None
conf = 'conf.json'
#configuration parameter checker.
with open(conf) as data_file:    
	data = json.load(data_file)
	if platform.system() == 'Windows':
		inkscapeex = data['inkscape'][0]['winexe']
	elif platform.system() == 'Linux':
		inkscapeex = data['inkscape'][1]['linux']
	if data['dropbox'][0]['enabled'] == 'true':
		dropbx = True
		db_token = data['dropbox'][1]['accesstoken']
		client = dropbox.Dropbox(db_token)
	else:
		dropbx = False
	if data['experimental']['autosubmit'] == 'true':
		autosubmit = True
	else:
		autosubmit = False
#Directory scanned for uploading to meleehd
updir = 'upload/'
if not os.path.exists(updir): os.makedirs(updir)
#Directory where textures are packed
bldir = 'packedtextures/'
if not os.path.exists(bldir): os.makedirs(bldir)
#This directory stores what was in the updir once it has been processed
comdir = 'submitted/'
if not os.path.exists(comdir): os.makedirs(comdir)
#opens firefox to a blank page before starting submit loop
if autosubmit == True:
	envi = ffhelper.env('default')
	browser = Browser('firefox', profile = envi)
#Creates and prepares a directory for the texture, including finding the matching sd texture.
def dirprep(img,name):
	print('Preparing directory for texture:\'%s\'' % name)
	sdsrc = name + '.png'
	source = updir + img
	path = bldir + name
	if not os.path.exists(path): os.makedirs(path)
	shutil.copy(source, path)
	print('Finding sd texture in sd texture source.')
	with zipfile.ZipFile('support/sdsource.zip', 'r') as myzip:
		tempdir = tempfile.mkdtemp()
		sdsource = myzip.extract(sdsrc,tempdir)
		shutil.move('%s/%s.png'%(tempdir,name), '%s/sd_%s.png'%(path,name))
	shutil.move(source, comdir+img)
#Creates an .svg from provided .ai/.pdf via inkscape.
def svgprep(img,name):
	print('Creating .svg from \'%s\' via inkscape.' % img)
	path = bldir + name
	os.system("%s --file=%s/%s --export-plain-svg=%s/%s.svg" % (inkscapeex,path,img,path,name))
#Creates a .png from .svg via inkscape if there isn't already a .png.
def pngprep(img,name):
	path = bldir + name
	if os.path.isfile('%s%s.png' % (updir, name)) == True:
		prerenderpng = '%s%s.png' % (updir, name)
		print('PNG detected.')
		shutil.copy(prerenderpng, path + '/%s.png' % name)
		shutil.move(prerenderpng, comdir+'%s.png' % name)
	else:
		print('PNG not detected, creating .png from \'%s\' via inkscape.' % img)
		os.system("%s --file=%s/%s --export-png=%s/%s.png" % (inkscapeex,path,name + '.svg',path,name))
#Handles uploading texture directory to dropbox.
def dbupload(name):
	upload = bldir + name
	client.file_create_folder(name)
	for x in os.listdir(upload):
		v = upload + '/' + x
		f = open(v, 'rb')
		client.put_file('/' + name + '/' + x, f)
	dburld = client.share('/%s/'%name, short_url=False)
	dburl = dburld.get('url')
	return dburl
#Handles uploading sd/hd texture to deviantArt, only returning src url.
def daupload(img, name, aname):
	im = bldir + name + '/' + aname
	dec = 'Official MeleeHD texture submission. MeleeHD is a community texture project, our official goal is to restore Nintendo\'s \'Super Smash Bros Melee\' with hires textures to be as close to the original as possible, if you want to know more about this project or want to get involved, send me a message, visit the official forums http://www.meleehd.boards.net, or check out a reddit post about the project https://www.reddit.com/r/SSBM/comments/3fl61i/melee_hd_wip/'
	imglink, weblink = da.uppub(aname,dec,im)
	return imglink, weblink
#Directs user to post thread, and prompts user to login if not already logged.
def pblogin():
	posturl = 'http://meleehd.boards.net/thread/new/3'
	browser.visit(posturl)
	ltest = browser.find_by_text('Login')
	title = browser.title
	if not ltest:
		print('')
		print('User logged in. Continuing.')
	else:
		print('User not logged in.')
		browser.click_link_by_text('Login')
		a = 0
		#starts loop to wait for user to login.
		while(title != 'Create Thread | Melee HD'):
			title = browser.title
			a = a + 1
			b = 'Waiting for user to login, to avoid this, login with firefox outside of script.' + '.' * a
			time.sleep(1)
		ltestloop()
#function only exists because I don't know how to otherwise make the login test restart to ensure the user is logged in.
def ltestloop():
	pblogin()
#Prepares .svg to be merged with forum body.
def svghelp(svg):
	data=None
	with open (svg, "r") as mysvg:
		data=mysvg.read()
	return data
#Prepares forum body for being injected via javascript by making it readable by javascript and the website.
def forumhelp(forumbody):
	data=forumbody.replace('\n', '<br>')
	data1=data.replace('"','\\'+'\"')
	finalbody = data1
	return finalbody
#Selects upload directory to scan for potential uploads and starts an upload loop.
uploads = os.listdir('upload')
for x in uploads:
	start = time.time()
	#splits up the texture from extension and name. example.png would be name = example, extension = png
	name = os.path.splitext(x)[0]
	extension = os.path.splitext(x)[1]
	a = extension
	#tests for what type of file is attempting to be uploaded.
	if a == '.ai':
		dirprep(x, name)
		svgprep(x, name)
	elif a == '.pdf':
		dirprep(x, name)
		svgprep(x, name)
	elif a == '.svg':
		dirprep(x, name)
		pass
	#If the upload candidate isn't an .ai/.pdf/.svg upload will be halted.
	elif a == '.png':
		continue
	else:
		print('Filetype \'%s\' not supported. Only .ai, .svg, and .pdf files are supported.')
		continue
	#render png via inkscape
	pngprep(x, name)
	dim = name.split('_')
	num = 0
	#parse file for original dimensions without having to use pillow library to get dimensions.
	for x in dim:
		num = num + 1
		if num == 2:
			bun = 0
			for y in x.split('x'):
				bun = bun + 1
				if bun == 1:
					xdim = y
				else:
					ydim = y
	xdim = int(xdim)
	ydim = int(ydim)
	#calculate hd resolution
	hdxdim = xdim *16
	hdydim = ydim *16
	nname = name + '.png'
	sname = 'sd_' + nname
	#upload to dropbox if it's enabled.
	if dropbx == True:
		dblink = dbupload(name)
	else:
		dblink = None
	#upload sd, and hd textures to deviantArt and retrieve links.
	dahd,hddeviantart_url = daupload(x, name, nname)
	dasd,sddeviantart_url = daupload(x, name, sname)
	#prepare svg for forum boxy.
	svglocation = bldir + name + '/'+ name +'.svg'
	svg = svghelp(svglocation)
	#write out forum body
	#note: to get % out, you need to put 2 %% as seen in the width parameter.
	svgfilesize = os.path.getsize(svglocation)
	pngfilesize = os.path.getsize('%s%s/%s' % (bldir, name, nname))
	l=lambda:defaultdict(l)
	profilelink, username = da.profile()
	texturedata = l()
	texturedata['info'] = {'name':nname}
	texturedata['texture']['sd'] = {'directlink':dasd,'dapage':sddeviantart_url,'x':str(xdim),'y':str(ydim)}
	texturedata['texture']['hd'] = {'directlink':dahd,'dapage':hddeviantart_url,'x':str(hdxdim),'y':str(hdydim), 'pngsize': pngfilesize, 'svg':svg, 'svgsize':svgfilesize}
	texturedata['deviantart'] = {'username':username,'profilelink':profilelink}
	if dropbx == True:
		texturedata['dropbox'] = {'project link':dblink}
	texturesubmitdata = bldir+name+'/'+name+'_postdata.json'
	with open(texturesubmitdata, 'w') as f:
		json.dump(texturedata, f, sort_keys = False, indent = 4,ensure_ascii=False)
	#prepare browser for forum post
	#parse paragraph to it's final form to be injected via javascript.
	#fill subject line of forum.
	#test for autosubmit status.
	bbcodesubmitdata = bldir+name+'/'+name+'_bbctemp.txt'
	with open(bbcodesubmitdata, 'w') as f:
		f.write(template.bbtemplate(texturedata))
	if autosubmit == True:
		pblogin()
		browser.fill('subject', nname)
		with browser.get_iframe(2) as iframe:
			iframe.execute_script("""

var forumBody = '%s';
document.getElementsByTagName('body')[0].innerHTML = forumBody;

""" % (final))
	#test whether or not a new page with the texture name has been submitted before moving on, note that splinter does not automatically press submit at the moment, this will change in the future when the script is close to 100% accurate.
		pagename = nname + ' | Melee HD'
		pagetitle = browser.title
		while(pagetitle != pagename):
			pagetitle = browser.title
			time.sleep(1)
	

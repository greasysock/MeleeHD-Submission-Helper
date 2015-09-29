import os
import shutil
from subprocess import call
import dropbox
import da
from splinter import Browser
import ffhelper
import time
import platform

db_token = None
conf = 'conf.json'
with open(conf) as data_file:    
	data = json.load(data_file)
	da_token = data['deviantart']['accesstoken']
	if platform.system() == 'Windows':
		inkscapeex = data['inkscape'][0]['winexe']
	elif platform.system() == 'Linux':
		inkscapeex = data['inkscape'][1]['linux']
	if data['dropbox'][0]['enabled'] == 'true':
		dropbx = True
		db_token = data['dropbox'][1]['access_token']
		client = dropbox.client.DropboxClient(db_token)
	else:
		dropbx = False
	if data['experimental']['autosubmit'] == 'true':
		autosubmit = True
	else:
		autosubmit = False
print da_token
print inkscapeex
print db_token
updir = 'upload/'
bldir = 'packedtextures/'
texres = 'sdtextures/'
comdir = 'submitted/'
envi = ffhelper.env('default')
browser = Browser('firefox', profile = envi)
def dirprep(img,name):
	sdsrc = texres + name + '.png'
	source = updir + img
	path = bldir + name
	if not os.path.exists(path): os.makedirs(path)
	shutil.copy(source, path)
	print('Finding sd texture in sd texture source.')
	shutil.copy(sdsrc, path + '/sd_%s.png' % name)
def svgprep(img,name):
	print('Creating .svg from \'%s\' via inkscape.' % img)
	path = bldir + name
	os.system("%s --file=%s/%s --export-plain-svg=%s/%s.svg" % (inkscapeex,path,img,path,name))
def pngprep(img,name):
	print('Creating .png from \'%s\' via inkscape.' % img)
	path = bldir + name
	os.system("%s --file=%s/%s --export-png=%s/%s.png" % (inkscapeex,path,name + '.svg',path,name))
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
def daupload(img, name, aname):
	test = da.test(da_token)
	if test == 'error':
		print('deviantArt Token Invalid.')
		exit()
	im = bldir + name + '/' + aname
	dec = 'Official MeleeHD texture submission. MeleeHD is a community texutre project, our official goal is to restore Nintendo\'s \'Super Smash Bros Melee\' with hires textures to be as close to the original as possible, if you want to know more about this project or want to get involved, send me a message, visit the official forums http://www.meleehd.boards.net, or check out a reddit post about the project https://www.reddit.com/r/SSBM/comments/3fl61i/melee_hd_wip/'
	imglink = da.uppub(aname,dec,im,da_token)
	return imglink
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
		while(title != 'Create Thread | Melee HD'):
			title = browser.title
			a = a + 1
			b = 'Waiting for user to login, to avoid this, login with firefox outside of script.' + '.' * a
			print '{}\r'.format(b),
			time.sleep(1)
		ltestloop()
def titletest(name):
	title = browser.title
	if title != name:
		return False
	else:
		return True
def ltestloop():
	pblogin()
def svghelp(svg):
	data=None
	with open (svg, "r") as mysvg:
		data=mysvg.read()
	return data
def forumhelp(forumbody):
	data=forumbody.replace('\n', '<br>')
	data1=data.replace('"','\\'+'\"')
	finalbody = data1
	return finalbody
uploads = os.listdir('upload')
for x in uploads:
	start = time.time()
	print x
	name = os.path.splitext(x)[0]
	extension = os.path.splitext(x)[1]
	a = extension
	print('Preparing directory for texture:\'%s\'' % name)
	if a == '.ai':
		dirprep(x, name)
		svgprep(x, name)
	elif a == '.pdf':
		dirprep(x, name)
		svgprep(x, name)
	elif a == '.svg':
		dirprep(x, name)
		print('pass')
	else:
		print('Filetype \'%s\' not supported. Only .ai, .svg, and .pdf files are supported.')
		exit()
	pngprep(x, name)
	dim = name.split('_')
	num = 0
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
	hdxdim = xdim *16
	hdydim = ydim *16
	nname = name + '.png'
	sname = 'sd_' + nname
	if dropbx = True:
		dblink = dbupload(name)
	else:
		dblink = None
	dahd = daupload(x, name, nname)
	dasd = daupload(x, name, sname)
	svglocation = bldir + name + '/'+ name +'.svg'
	svg = svghelp(svglocation)
	paragraph = '''Original Texture: %sx%s
<div class="quote no_header"><div class="quote_body"><img alt="" src="%s" height"%s" width="%s" style="max-width:1600%%;">
<div class="quote_clear"></div></div></div>HD Texture: %sx%s
<div class="quote no_header"><div class="quote_body"><img alt="" src="%s" style="max-width:100%%;">
<div class="quote_clear"></div></div></div>

SVG:

<code>%s</code>

<a rel="nofollow" target="_blank" href="%s">Project Files

</a>File size not optimized.

Post created in %s seconds''' % (str(xdim),str(ydim),dasd,str(hdxdim),str(hdydim),str(hdxdim),str(hdydim),dahd,svg,dblink,time.time()-start)
	pblogin()
	final = forumhelp(paragraph)
	time.sleep(1)
	browser.fill('subject', nname)
	time.sleep(1)
	if autosubmit = True:
		with browser.get_iframe(2) as iframe:
			iframe.execute_script("""

var forumBody = '%s';
document.getElementsByTagName('body')[0].innerHTML = forumBody;

""" % (final))
	pagename = nname + ' | Melee HD'
	pagetitle = browser.title
	while(pagetitle != pagename):
			pagetitle = browser.title
			time.sleep(1)
	

from support import conf
def bbtemplate(dictionary):
	texturename = dictionary['info']['name']
	daprofile = dictionary['deviantart']['profilelink']
	dausername = dictionary['deviantart']['username']
	sdimg = dictionary['texture']['sd']['directlink']
	sddeviantart = dictionary['texture']['sd']['dapage']
	hdimg = dictionary['texture']['hd']['directlink']
	hdsize = dictionary['texture']['hd']['pngsize']
	hddeviantart = dictionary['texture']['hd']['dapage']
	hdx = dictionary['texture']['hd']['x']
	hdy = dictionary['texture']['hd']['y']
	svg = dictionary['texture']['hd']['svg']
	svgsize = dictionary['texture']['hd']['svgsize']
	if conf.db_client() == True:
		dblink = dictionary['dropbox']['project link']
		pjfiles = '''[font size="4"]
Author comments ↓[/font]

For the purpose of redundancy, the project files for this texture have been uploaded to [a href="{}"]Dropbox[/a].

This is a personal choice, and you don't have to do the same.
		'''.format(dblink)
	else:
		pjfiles = ''
	bbtemplate = u'''[font size="4"]Texture information table ↓[/font]


[table style="border:1px solid;border-collapse:separate;border-spacing:25px;text-align:left;"]
[tbody]
[tr style="text-decoration:underline;font-size:14px;"]
[th]Attribute[/th]
[th]Value[/th]
[/tr][tr]
[td]Texture name:[/td][td]{}[/td]
[/tr][tr]
[td]Short description:[/td][td][/td]
[/tr][tr]
[td]Artist's dA profile:[/td][td][a href="{}"][{}][/a][/td]
[/tr][tr]
[td]Links to unedited PNG:[/td][td][a href="{}"][image][/a], [a href="{}"][dA page][/a][/td]
[/tr][tr]
[td]Links to HD PNG:[/td][td][a href="{}"][image][/a], [a href="{}"][dA page][/a][/td]
[/tr][tr]
[td]HD PNG resolution:[/td][td]{} x {}[/td]
[/tr][tr]
[td]HD PNG file size:[/td][td]{} bytes (unoptimized)[/td]
[/tr][tr]
[td]SVG XML size:[/td][td]{} bytes[/td]
[/tr][tr]
[td]Forum users notified:[/td][td]{}[/td]
[/tr][tr]
[/tr]
[/tbody]
[/table]
{}

[font size="4"]Unedited ↓

[quote][img width="100%" src="{}" style="max-width:{}px;"][/quote]
Retexture ↓

[quote][img style="max-width:{}px;" src="{}.png" width="100%"][/quote]
Comparison ↓ (mouseover to view)

[quote style="background:hovergrid;"][img src="{}" style="max-width:{}px;" width="100%"][img width="100%" style="max-width:{}px;" src="{}"][/quote]
SVG XML code ↓

[/font]
[pre style="width:5000%;"][code]{}[/code][/pre]
[font size="4"]
Viewing the SVG ↓
[/font]

[quote author="@meleehd"]
To view the above code as a vector image:
[ul]
[li][b]Copy[/b] the code to your clipboard.[/li][li][b]Paste[/b] it into a text editor like [b]Notepad[/b].[/li][li][b]Save[/b] it with a name that ends in [b].svg[/b].[/li][li][b]Don't[/b] forget the dot in front. That's [b].svg[/b].[/li][li][b]Double-click[/b] on the file to make it open.[/li]
[/ul]You're done!

If the file doesn't open, [a href="https://inkscape.org/en/download/windows/"][b]install Inkscape[/b][/a] and try these steps again.[/quote]'''.format(texturename, daprofile, dausername, sdimg, sddeviantart, hdimg, hddeviantart, hdx, hdy, hdsize, svgsize, conf.bbcode_notify(), pjfiles, sdimg, hdx, hdx, hdimg, sdimg, hdx, hdx, hdimg, svg)
	return bbtemplate

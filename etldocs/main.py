from lxml import etree
import requests, json
import os

# Enviornment Variable Requirements:
# export CONFLUENCE_HOST="http://192.168.33.51:8090/confluence"
# export CONFLUENCE_USER="admin"
# export CONFLUENCE_USERPw="docker"
# export DATA_MOUNT_DIR="/Users/primusdj/github/rc_rancher/etldocs/docsData"
# 

# print( os.environ )


def main():
	"""
		We will want to use env_variables for the details on auth()... 
		also the url is the CNI address given by rancher...  perhaps a "link" option would be a better option?
		
		TcpIpAddress = '10.42.251.209:8090'
		host_url: http://10.42.251.209:8090/confluence
		restApi = '/confluence/rest/api/content'
		
		...
		http://192.168.33.50:8090/confluence/rest/api/content/65593?expand=body.view
		http://192.168.33.50:8090/confluence/rest/api/content/65596?expand=body.view
		http://192.168.33.51:8090/confluence/rest/api/content/65600?expand=body.view

	"""
	authUser = ( os.environ.get('CONFLUENCE_USER'), os.environ.get( 'CONFLUENCE_USERPW' ) )
	# r = requests.get( '/rest/api/content?type=page&spaceKey=RC', auth=('admin','docker'))
	confluence_url = '{}/rest/api/content?type=page&spaceKey=RC'.format( os.environ.get( 'CONFLUENCE_HOST' ) )
	
	# get a list of all of the pages that belong to the 'rc' space
	r = requests.get( confluence_url , auth=authUser)

	# print( json.dumps( r.json,indent=2,sort_keys=True ) )

	data = json.loads(r.text)

	# print( json.dumps( data,indent=2,sort_keys=True ) )

	for r in data['results']:

		if r['title'] !='rc':
			# change this to pull in the ids for the pages we need...
			pageQry = '?expand=body.view'
			pageUrl = str( r['_links']['self'] )
			rUrl = '{}{}'.format( pageUrl, pageQry )
			# print( rUrl )
			
			rPage = requests.get( rUrl, auth=authUser )

			pageData = json.loads( rPage.text )

			docTitle = pageData['title']
			htmlBody = etree.HTML( pageData['body']['view']['value'] )

			# print( etree.tostring(htmlBody, pretty_print=True ) )
			xpathGetContent = '//*/div[@class="columnLayout two-left-sidebar"]'
			xpathCountContent = 'count(//*/div[@class="columnLayout two-left-sidebar"])'

			# contentTree = body.xpath( xpathGetContent )
			elementCount = int( htmlBody.xpath( xpathCountContent ) )

			# print( json.dumps( pageData, indent=2, sort_keys=True ) )
			# HERE we would add template differentiation... clearly counting elements is a bad appraoch..
			if elementCount == 6:
				templateOrigional( docTitle, htmlBody, elementCount )
			elif elementCount == 3:
				serviceDocumentation( docTitle, htmlBody, elementCount )


def serviceDocumentation( pageTitle, pageDom, eCount=3 ):
	"""The service template all in one source of documentation..."""
	template = "single_source"
	publicXpath= "//*/p/text()"
	templatePublic = 'PUBLIC'

# 
# 	NOTE:  The code doesn't work, using the body content of the api pull has changed the structure of the DOM.
# 		Because we RC isn't going to go this direction with their document system structures we will now have
# 		to pull from another system all together.
# 


	# validatePublic = pageDom.xpath( publicXpath )[0]
	validatePublic = pageDom.xpath( publicXpath )
	print( validatePublic )
	if validatePublic == templatePublic:
		rowCountXpath= "count(//*[@id='main-content']/div/div[1]/div[2]/div/div[1]/table/tbody/tr)"
		rowCount = int( pageDom.xpath( rowCountXpath ) ) 
		publicDictionary = {}
		for index in range( 2, rowCount+1 ):
			rowKeyXpath= "//*[@id='main-content']/div/div[1]/div[2]/div/div[1]/table/tbody/tr[{}]/td[1]/text()".format( str( index ) )
			rowValueXpath= "//*[@id='main-content']/div/div[1]/div[2]/div/div[1]/table/tbody/tr[{}]/td[2]/text()".format( str( index ) )
			key = pageDom.xpath( rowKeyXpath )
			value = pageDom.xpath( rowValueXpath )

			publicDictionary[key[0]]=value[0]

		publicFile = os.path.join( __data_mount_dir__, template, templatePublic, "{}.json".format( pageTitle.replace(" ","_") ) )
		writeToDisk( publicDictionary, publicFile )

	# //*[@id="main-content"]/div/div[2]/div[1]/div/p
	userXpath= "//*[@id='main-content']/div/div[2]/div[1]/div/p/text()"
	templateUser = "USER"
	validateUser = pageDom.xpath( userXpath )[0]
	if validateUser == templateUser:
		rowCountXpath= "count(//*[@id='main-content']/div/div[2]/div[2]/div/div[1]/table/tbody/tr)"
		rowCount = int( pageDom.xpath( rowCountXpath ) ) 
		publicDictionary = {}
		for index in range( 2, rowCount+1 ):
			rowKeyXpath= "//*[@id='main-content']/div/div[2]/div[2]/div/div[1]/table/tbody/tr[{}]/td[1]/text()".format( str( index ) )
			rowValueXpath= "//*[@id='main-content']/div/div[2]/div[2]/div/div[1]/table/tbody/tr[{}]/td[2]/text()".format( str( index ) )
			rowSourceXpath= "//*[@id='main-content']/div/div[2]/div[2]/div/div[1]/table/tbody/tr[{}]/td[3]/text()".format( str( index ) )
			key = pageDom.xpath( rowKeyXpath )
			value = pageDom.xpath( rowValueXpath )
			# print(key, value)
			source = pageDom.xpath( rowSourceXpath )
			print(key, source.replace('\n',None))

		# 	publicDictionary[key[0]]=[value[0], source[0] if True else None]

		print( publicDictionary )

		userFile = os.path.join( __data_mount_dir__, template, templateUser, "{}.json".format( pageTitle.replace(" ","_") ) )
		writeToDisk( publicDictionary, userFile )


def templateOrigional( pageTitle, pageDom, eCount=6 ):
	"""The Template Origional"""
	template = "origional"
	docDictionary=dict()
	
	for index in range( 1, eCount+1 ):

		keyXpath ="//*[@id='main-content']/div/div[{}]/div[1]/div/p/text()".format( str( index ) )
		valueXpath ="//*[@id='main-content']/div/div[{}]/div[2]/div/p/text()".format( str( index ) )
		
		key = pageDom.xpath( keyXpath )
		value = pageDom.xpath( valueXpath )
		if not key:
			keyXpath ="//*[@id='main-content']/div/div[{}]/div[1]/div/p/span/text()".format(str(index))
			key = pageDom.xpath( keyXpath )

		if value:
			docDictionary[key[0]]=value[0]
		else:
			break
	
	print(docDictionary)
	# make json and write to file
	file = os.path.join( __data_mount_dir__, template, "{}.json".format( pageTitle.replace( " ","_" ) ) )
	writeToDisk( docDictionary, file )


def writeToDisk( docDict, file):
	"""Because i don't want to have to dub myself"""
	
	if not os.path.exists( os.path.dirname( file ) ):
		try:
			os.makedirs( os.path.dirname( file ) )
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	
	with open( file, 'w+' ) as f:
		json.dump( docDict, f, separators=(',',':'), sort_keys=True, indent=2 )
	

if __name__=="__main__":
	"""Lets get this application setup..."""
	if os.environ.get( "DATA_MOUNT_DIR" ):
		__data_mount_dir__ = os.path.join( os.environ.get( "DATA_MOUNT_DIR" ) )
	else:
		__data_mount_dir__ = os.path.join( os.path.realpath( os.path.join( os.getcwd(), os.path.dirname(__file__) ) ), "docsData" )

	main()

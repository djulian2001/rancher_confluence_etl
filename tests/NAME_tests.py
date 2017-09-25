import unittest
import NAME

class NAMETests( unittest.TestCase ):
	"""docstring for ClassName"""

	def setUp( self ):
		print "SETUP!"

	def tearDown( self ):
		print "TEAR Down!"

	def test_basic( self ):
		print "I Ran!"

if __name__ == '__main__':
	unittest.main()

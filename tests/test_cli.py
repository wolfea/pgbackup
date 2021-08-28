import pytest
from pgbackup import cli  

# $ pgbackup postgres://bob@example.com:5432/db_one --driver s3 backups

# $ pgbackup postgres://bob@example.com:5432/db_one --driver local /var/local/db_one/backups

url="postgres://bob@example.com:5432/db_one"

@pytest.fixture()
def parser(): 				#fixture function
	
	return cli.create_parser() 	

def test_parser_without_driver(parser):
	
	#without a specified driver the parser will exit 
	
	with pytest.raises(SystemExit):
		parser.parse_args([url]) 

def test_parser_with_driver(parser):
	
	#The parser will exit if it receives a driver
	#without a destination
	
	with pytest.raises(SystemExit):
		parser.parse_args([url, "--driver", "local"])

#happy test case 
def test_parser_with_driver_and_destination(parser):

	#The parser will not exit if it receives a driver 
	#with a destination 

	args=parser.parse_args([url,"--driver","local","/some/path"])
	assert args.url==url	
	assert args.driver=="local"
	assert args.destination=="/some/path"

def test_parser_with_unknown_driver(parser):
	
	#The parser will exit if the driver name is unknown
	
	with pytest.raises(SystemExit):
		parser.parse_args([url, "--driver", "azure", "destination"])

#happy test case 
def test_parser_with_known_drivers(parser):

	#The parser will not exit if the driver name is known
	
	for driver in ['local', 's3']:
		assert parser.parse_args([url, "--driver", driver, "destination"])  

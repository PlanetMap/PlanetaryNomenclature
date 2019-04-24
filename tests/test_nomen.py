''' Route/View Testing '''

def test_home(active_client):
    ''' homepage view '''
    rv = active_client.get('/')
    assert b'Welcome' in rv.data

def test_intro(active_client):
    ''' /Page/Introduction view '''
    rv = active_client.get('/Page/Introduction')
    assert b'Introduction' in rv.data

def test_history(active_client):
    ''' /Page/History view '''
    rv = active_client.get('/Page/History')
    assert b'History of Planetary Nomenclature' in rv.data

def test_approved(active_client):
    ''' /Page/Approved view '''
    rv = active_client.get('/Page/Approved')
    assert b'How Names are Approved' in rv.data

def test_members(active_client):
    ''' /Page/Members view '''
    rv = active_client.get('/Page/Members')
    assert b'IAU Working Group and Task Group Members' in rv.data

def test_faq(active_client):
    ''' /Page/FAQ view '''
    rv = active_client.get('/Page/FAQ')
    assert b'Frequently Asked Questions' in rv.data

def test_acknowledgements(active_client):
    ''' /Page/Acknowledgements view '''
    rv = active_client.get('/Page/Acknowledgements')
    assert b'Acknowledgements' in rv.data

def test_relatedresources(active_client):
    ''' /Page/Related_Resources view '''
    rv = active_client.get('/Page/Related_Resources')
    assert b'Related Resources' in rv.data

def test_contact(active_client):
    ''' /Page/Contact_Us view '''
    rv = active_client.get('/Page/Contact_Us')
    assert b'Contact Us' in rv.data

def test_iaurules(active_client):
    ''' /Page/Rules view '''
    rv = active_client.get('/Page/Rules')
    assert b'IAU Rules and Conventions' in rv.data

def test_gazspecifics(active_client):
    ''' /Page/Specifics view '''
    rv = active_client.get('/Page/Specifics')
    assert b'Specifics of the Gazetteer' in rv.data

def test_abbreviations(active_client):
    ''' /Abbreviations view '''
    rv = active_client.get('/Abbreviations')
    assert b'Abbreviations for Continents, Countries, and Ethnic Groups' in rv.data

def test_references(active_client):
    ''' /References view '''
    rv = active_client.get('/References')
    assert b'Sources of Planetary Names' in rv.data

def test_categories(active_client):
    ''' /Page/Categories view '''
    rv = active_client.get('/Page/Categories')
    assert b'Categories for Naming Features on Planets and Satellites' in rv.data

def test_descriptorterms(active_client):
    ''' /DescriptorTerms view '''
    rv = active_client.get('/DescriptorTerms')
    assert b'Descriptor Terms (Feature Types)' in rv.data

def test_targetcoordinates(active_client):
    ''' /TargetCoordinates view '''
    rv = active_client.get('/TargetCoordinates')
    assert b'Coordinate Systems for Planets and Satellites' in rv.data

def test_webhelp(active_client):
    ''' /Page/Website view '''
    rv = active_client.get('/Page/Website')
    assert b'Help using this Website' in rv.data

def test_images(active_client):
    ''' /Page/Images view '''
    rv = active_client.get('/Page/Images')
    assert b'Images Showing Locations of Named Features' in rv.data

def test_gisdownloads(active_client):
    ''' /GIS_Downloads view '''
    rv = active_client.get('/GIS_Downloads')
    assert b'KML and Shapefile Downloads' in rv.data

def test_advancedsearch(active_client):
    ''' /AdvancedSearch view '''
    rv = active_client.get('/AdvancedSearch')
    assert b'Advanced Nomenclature Search' in rv.data

def test_namerequest(active_client):
    ''' /FeatureNameRequest view '''
    rv = active_client.get('/FeatureNameRequest')
    assert b'Name Request Form' in rv.data


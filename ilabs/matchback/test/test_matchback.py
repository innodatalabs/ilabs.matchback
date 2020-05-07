import lxml.etree as et
from ilabs.matchback.main import matchback


def test_matchback():
    html = et.fromstring(b'''<body>
    <p id="para1">Hello, world!</p>
</body>
''')
    innodom = et.fromstring(b'''<dom xmlns="http://innodatalabs.com/innodom">
<content>
<p id="id1">Hello, world!</p>
</content>
<meta>
<datapoint key="name" idref="id1">Mike</datapoint>
</meta>
</dom>\
''')

    meta = matchback(html, innodom)

    assert len(meta) == 1
    assert meta[0]['idref'] == 'para1'
    assert meta[0]['xpath'] == '/body/p'


def test_matchback01():
    html = et.fromstring(b'''<body>
    <p id="para1"><b>Hello,</b> world!</p>
</body>
''')
    innodom = et.fromstring(b'''<dom xmlns="http://innodatalabs.com/innodom">
<content>
<p id="id1">Hello, world!</p>
</content>
<meta>
<datapoint key="name" idref="id1">Mike</datapoint>
</meta>
</dom>\
''')

    meta = matchback(html, innodom)

    assert len(meta) == 1
    assert et.tostring(html) == b'''<body>
    <p id="para1"><b>Hello,</b> world!</p>
</body>\
'''
    assert meta[0]['idref'] == 'para1'
    assert meta[0]['xpath'] == '/body/p'

from ilabs.matchback.main import segment

def test_segment():

    assert segment('Hello, world!') == ['Hello,', 'world!']
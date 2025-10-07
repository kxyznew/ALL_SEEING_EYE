from app.services.youtube import validate_youtube_url

def test_validate_youtube_url():
    assert validate_youtube_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    assert validate_youtube_url('https://youtu.be/dQw4w9WgXcQ')
    assert not validate_youtube_url('https://example.com/watch?v=dQw4w9WgXcQ')

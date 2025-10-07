from app.services.summarize import simple_extractive_summary, generate_key_points

def test_simple_extractive_summary_basic():
    lines = ['short', 'this is a much longer sentence about topic', 'another long line that should be considered important', 'short too']
    res = simple_extractive_summary(lines, max_points=2)
    assert len(res) == 2
    assert any('longer sentence' in r or 'another long line' in r for r in res)

def test_generate_key_points_fallback():
    lines = ['a line that is meaningful and has sufficient length to count', 'another content line that should be summarized into key points']
    res = generate_key_points(lines, max_points=3)
    assert len(res) >= 1

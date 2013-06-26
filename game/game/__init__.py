from .levels import TestLevel


class TestGame(object):
    """TestGame"""
    
    assets = [
        'audio/ThisUsedToBeACity.ogg',
        'audio/beep.ogg',
        'shaders/basic.f.glsl',
        'shaders/basic.v.glsl',
    ]

    levels = [
        TestLevel,
    ]
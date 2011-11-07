#! /usr/bin/env python
from RenderWorld import RenderWorld
import sys

if __name__ == '__main__':
    if len(sys.argv) == 0:
        RENDER = RenderWorld(sys.argv[1])
    else:
        RENDER = RenderWorld(None)

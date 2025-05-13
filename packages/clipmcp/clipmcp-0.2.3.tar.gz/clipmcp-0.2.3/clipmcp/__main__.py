#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主入口模块
使clipmcp包可以直接作为模块运行
"""

import sys
from clipmcp.cli import main

if __name__ == "__main__":
    sys.exit(main()) 
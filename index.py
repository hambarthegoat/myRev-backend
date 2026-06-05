import sys
import os

# Ensure Vercel can find the 'app' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# Vercel Serverless Function entry point

from django.test import TestCase

# Create your tests here.
import sys
for i in range(len(sys.path)):
    print(sys.path[i])

import django

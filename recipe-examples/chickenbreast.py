#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
http://www.seriouseats.com/2015/07/the-food-lab-complete-guide-to-sous-vide-chicken-breast.html
"""

import anova

cooker = anova.AnovaCooker('', '')
print(cooker.create_job(temperature=66, seconds=60 * 60, temperature_unit='c'))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
http://recipes.anovaculinary.com/recipe/sous-vide-egg-bites-bacon-gruyere
"""

import anova

cooker = anova.AnovaCooker('', '')
print(cooker.create_job(temperature=77.8, seconds=60 * 60, temperature_unit='c'))

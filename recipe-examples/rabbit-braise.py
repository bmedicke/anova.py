#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://stefangourmet.com/2015/03/25/rabbit-sous-vide-time-and-temperature/
"""

import anova

cooker = anova.AnovaCooker('', '')
print(cooker.create_job(temperature=75, seconds=28800, temperature_unit='c'))

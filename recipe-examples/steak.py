#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://www.chefsteps.com/activities/sous-vide-time-and-temperature-guide
"""

import anova

cooker = anova.AnovaCooker('', '')
print(
    cooker.create_job(
        temperature=54, seconds=60 * 60 * 2, temperature_unit='c'))

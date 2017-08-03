#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://www.chefsteps.com/activities/the-egg-calculator
"""

import anova

cooker = anova.AnovaCooker('', '')
print(cooker.create_job(temperature=71, seconds=60 * 17, temperature_unit='c'))

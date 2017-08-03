#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to interface with the the Anova Precision Cooker API.
"""

import json
from typing import Union

import requests


class AnovaCooker:
    """
    you will need to pass your cooker_id and the corresponding secret.
    the easiest way to get them is with mitmproxy. see readme.md for more info.
    """

    def __init__(self, cooker_id: str, secret: str) -> None:
        """
        TODO: stop spoofing user agent
        """
        base_url = "https://api.anovaculinary.com/cookers/"
        self._url = base_url + cooker_id + "?secret=" + secret
        self._jobs_url = base_url + cooker_id + "/jobs?secret=" + secret
        self._headers = {
            'User-Agent': 'Cook/1.2.2 (iPhone; iOS 10.2; Scale/2.00)'
        }

    @property
    def current_temperature(self) -> Union[int, float]:
        return self.get_status_object()['current_temp']

    @property
    def target_temperature(self) -> Union[int, float]:
        return self.get_status_object()['target_temp']

    @target_temperature.setter
    def target_temperature(self, temperature: Union[int, float]) -> str:
        payload = {'target_temp': temperature}
        self._post_request(self._url, payload)

    @property
    def temperature_unit(self) -> str:
        """
        valid values are:
        'c' for celsius,
        'f' for Fahrenheit and
        '' for the currently set default unit.
        """
        return self.get_status_object()['temp_unit']

    @temperature_unit.setter
    def temperature_unit(self, unit: str):
        if unit not in ('c', 'f', ''):
            raise ValueError(
                "temperature_unit has to be either 'c', 'f' or ''")

        payload = {'temp_unit': unit}
        self._post_request(self._url, payload)

    @property
    def running(self) -> bool:
        """
        starts or stops the cooker.
        """
        return self.get_status_object()['is_running']

    @running.setter
    def running(self, state: bool):
        payload = {'is_running': state}
        self._post_request(self._url, payload)

    @property
    def speaker_mode(self) -> bool:
        """
        setting this to False disables all beeps.
        hurrah for late night cooking!
        be careful it also disables the minimum water level beeping.
        """
        return self.get_status_object()['speaker_mode']

    @speaker_mode.setter
    def speaker_mode(self, state: bool):
        payload = {'speaker_mode': state}
        self._post_request(self._url, payload)

    def _get_request(self, url: str) -> str:
        request = requests.get(url, headers=self._headers)
        return json.dumps(request.json(), indent=4, sort_keys=True)

    def _post_request(self, url: str, payload: dict) -> str:
        request = requests.post(url, json=payload, headers=self._headers)
        return json.dumps(request.json(), indent=4, sort_keys=True)

    def _set_timer(self, seconds: Union[int, float]) -> str:
        """
        calling this on its own does nothing. use create_job() instead.
        """
        payload = {'timer_length': seconds}
        return self._post_request(self._jobs_url, payload)

    def stop_alarm(self) -> str:
        """
        disables the alarm that signals the end of a cook.
        """
        payload = {"alarm_active": False}
        return self._post_request(self._url, payload)

    def get_status(self) -> str:
        """
        returns current state as json.
        """
        return self._get_request(self._url)

    def get_status_object(self) -> dict:
        """
        returns current status as a dictionary.
        """
        return json.loads(self.get_status())['status']

    def get_jobs(self) -> str:
        """
        returns all jobs (including past ones) as json.
        """
        return self._get_request(self._jobs_url)

    def get_jobs_object(self) -> dict:
        """
        returns all jobs (including past ones) as a dictionary.
        """
        return json.loads(self.get_jobs())

    def create_job(self,
                   temperature: Union[int, float],
                   seconds: Union[int, float],
                   temperature_unit: str='') -> str:
        """
        passing temperature_unit is preferred since it is faster
        (skips request for current value) and avoids ambiguity in shared code.
        """

        if not temperature_unit:
            temperature_unit = self.temperature_unit

        self.target_temperature = temperature
        self._set_timer(seconds)

        temp_unit_expansion = {'c': 'Celsius', 'f': 'Fahrenheit'}
        payload = {
            'is_running': False,
            'job_id': '',
            'job_info': {
                'display_item_identifier': '',
                'duration': seconds,
                'source': 'user_defined',
                'source_identifier': '',
                'temperature': temperature,
                'temperature_unit': temp_unit_expansion[temperature_unit]
            },
            'job_stage': 0,
            'job_type': 'manual_cook',
            'max_circulation_interval': 0,
            'target_temp': temperature,
            'temp_unit': temperature_unit,
            'threshold_temp': 0,
            'timer_length': seconds
        }

        return self._post_request(self._jobs_url, payload)

# tests/unit/test_sun_calendar_generate_and_query.py

import os

import numpy as np
import pytest

from time_engine.sun_calendar import SunCalendar
from time_engine.time import Time


@pytest.mark.unit
class TestSunCalendarUnit:
    def test_generate_sun_table_dimensions(self):
        """
        Ensure the sun table matches the time configuration dimensions.
        """
        t = Time(hours_per_day=24, days_per_month=30, months_per_year=1)
        calendar = SunCalendar(t)
        calendar.generate()
        assert calendar.sun_table.shape == (30, 24)

    def test_altitude_bounds(self):
        """
        Ensure that altitude interpolation returns a float and remains within valid range.
        """
        t = Time(hours_per_day=24, days_per_month=1, months_per_year=1)
        calendar = SunCalendar(t)

        val = calendar.altitude(0, 12)
        assert isinstance(val, float)
        # Allow a tiny tolerance around the expected [-90, 90] range
        assert -90.0 - 1e-3 <= val <= 90.0 + 1e-3

    def test_altitude_edge_cases(self):
        """
        Query edge values to ensure no index errors.
        """
        t = Time(hours_per_day=24, days_per_month=30, months_per_year=1)
        calendar = SunCalendar(t)

        for day, hour in [(0, 0), (29, 23), (15, 0), (0, 23)]:
            val = calendar.altitude(day, hour)
            assert isinstance(val, float)

    def test_save_and_load_cycle(self, tmp_path):
        """
        Test saving and reloading the sun table to ensure persistence.
        """
        t = Time(hours_per_day=12, days_per_month=10, months_per_year=1)
        calendar = SunCalendar(t)

        file_path = tmp_path / "sun_test.npy"
        calendar.save(str(file_path))
        assert file_path.exists()

        calendar.sun_table = np.zeros_like(calendar.sun_table)  # Reset to dummy values
        calendar.load(str(file_path))  # <- This method must exist in SunCalendar

        loaded = calendar.sun_table
        assert np.allclose(loaded, calendar.sun_table)

from collections.abc import Callable
from datetime import date as Date
from datetime import datetime as Dt
from datetime import time as Time
from datetime import timedelta as Δ
from functools import partial, reduce

import pytest
from str2td import str2td

tz = Dt.now().astimezone().tzinfo

f = partial(str2td, tz=tz)


@pytest.mark.parametrize(
	("case_fn",),
	(
		(str.upper,),
		(str.lower,),
		(str.title,),
		(lambda s: s,),
	),
)
@pytest.mark.parametrize(
	("m",),
	(
		(1,),
		(2,),
		(3,),
		(7,),
		(10,),
	),
)
def test_robostr_one_unit(*, m: int, case_fn: Callable[[str], str]):
	f2 = partial(f, now=Dt.now(tz=tz))

	f2 = lambda s, f2=f2: f2(case_fn(s))

	if now_1s := Δ(seconds=1) * m:
		assert f2(f"{m}s") == now_1s
		assert f2(f"{m}sec") == now_1s
		assert f2(f"{m}secs") == now_1s
		assert f2(f"{m}sex") == now_1s
		assert f2(f"{m}second") == now_1s
		assert f2(f"{m}seconds") == now_1s

	if now_1m := Δ(minutes=1) * m:
		assert f2(f"{m}m") == now_1m
		assert f2(f"{m}min") == now_1m
		assert f2(f"{m}mins") == now_1m
		assert f2(f"{m}minute") == now_1m
		assert f2(f"{m}minutes") == now_1m

	if now_1h := Δ(hours=1) * m:
		assert f2(f"{m}h") == now_1h
		assert f2(f"{m}hr") == now_1h
		assert f2(f"{m}hrs") == now_1h
		assert f2(f"{m}hour") == now_1h
		assert f2(f"{m}hours") == now_1h

	if now_1d := Δ(days=1) * m:
		assert f2(f"{m}d") == now_1d
		assert f2(f"{m}day") == now_1d
		assert f2(f"{m}days") == now_1d

	if now_1w := Δ(days=7) * m:
		assert f2(f"{m}w") == now_1w
		assert f2(f"{m}week") == now_1w
		assert f2(f"{m}weeks") == now_1w

	if now_1y := Δ(days=365) * m:
		assert f2(f"{m}y") == now_1y
		assert f2(f"{m}year") == now_1y
		assert f2(f"{m}years") == now_1y

	if now_1decade := Δ(days=365 * 10) * m:
		assert f2(f"{m}decade") == now_1decade
		assert f2(f"{m}decades") == now_1decade

	if now_1rescue := Δ(hours=6) * m:
		assert f2(f"{m}res") == now_1rescue
		assert f2(f"{m}reses") == now_1rescue
		assert f2(f"{m}resees") == now_1rescue
		assert f2(f"{m}rescue") == now_1rescue
		assert f2(f"{m}rescues") == now_1rescue

	if now_1pull := Δ(hours=11, minutes=30) * m:
		assert f2(f"{m}pul") == now_1pull
		assert f2(f"{m}pull") == now_1pull
		assert f2(f"{m}puls") == now_1pull
		assert f2(f"{m}pulls") == now_1pull
		assert f2(f"{m}card") == now_1pull
		assert f2(f"{m}cards") == now_1pull


def test_robostr_many_units():
	f2 = partial(f, now=Dt.now(tz=tz))

	assert f2("1h!30m!-.25m") == f2("1h30m-.25m") == Δ(hours=1) + Δ(minutes=30) + Δ(minutes=-0.25)
	assert f2("1s!-1s") == f2("1s-1s") == Δ(seconds=1) + Δ(seconds=-1)


@pytest.mark.parametrize(
	("case_fn",),
	(
		(str.lower,),
		(str.upper,),
		(str.title,),
		(lambda s: s,),
	),
)
@pytest.mark.parametrize(
	("dt", "expected_offset"),
	(
		(Dt(2025, 5, 12, 10, 0, 0, tzinfo=tz), 0),
		(Dt(2025, 2, 28, 10, 0, 0, tzinfo=tz), 3),
		(Dt(2024, 2, 29, 10, 0, 0, tzinfo=tz), 4),
		(Dt(2024, 12, 1, 10, 0, 0, tzinfo=tz), 1),
		(Dt(2024, 1, 10, 10, 0, 0, tzinfo=tz), 5),
	),
)
def test_weekday(*, dt: Dt, expected_offset: int, case_fn: Callable[[str], str]):
	f2 = partial(f, now=dt)

	f2 = lambda s, f2=f2: f2(case_fn(s))

	assert f2("mon") == f2("monday") == Δ(days=(expected_offset) % 7 or 7)
	assert f2("tue") == f2("tuesday") == Δ(days=(expected_offset + 1) % 7 or 7)
	assert f2("wed") == f2("wednesday") == Δ(days=(expected_offset + 2) % 7 or 7)
	assert f2("thu") == f2("thursday") == Δ(days=(expected_offset + 3) % 7 or 7)
	assert f2("fri") == f2("friday") == Δ(days=(expected_offset + 4) % 7 or 7)
	assert f2("sat") == f2("saturday") == Δ(days=(expected_offset + 5) % 7 or 7)
	assert f2("sun") == f2("sunday") == Δ(days=(expected_offset + 6) % 7 or 7)
